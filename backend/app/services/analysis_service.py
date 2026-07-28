import json
import logging
import re
from pathlib import Path
from collections import defaultdict

from app.core.config import RAG_CONTEXT
from app.core.groq_client import ask_groq
from app.rag.retriever import Retriever
from app.services.dependency_analyzer import DependencyAnalyzer
from app.services.markdown_formatter import MarkdownFormatter
from app.services.repository_scanner import RepositoryScanner
from app.analyzers.repository_intelligence import (
    RepositoryIntelligence,
)

logger = logging.getLogger(__name__)


class AnalysisService:

    DATA_DIR = Path("../data")

    _repository_intelligence_cache = {}

    def _repository_intelligence(
        self,
        repository: str,
    ):
        """
        Analyze the repository and cache the result.
        """

        if repository in self._repository_intelligence_cache:
            logger.info(
                "Using cached repository intelligence for %s",
                repository,
            )
            return self._repository_intelligence_cache[
                repository
            ]

        repository_path = (
            self.DATA_DIR / repository
        )

        analyzer = RepositoryIntelligence(
            repository_path
        )

        intelligence = analyzer.analyze()

        self._repository_intelligence_cache[
            repository
        ] = intelligence

        return intelligence

    def _get_retriever(
        self,
        repository: str,
    ) -> Retriever:
        """
        Return a Retriever instance for the repository.
        """
        return Retriever(repository)

    def _get_project_context(
        self,
        repository: str,
        k: int,
    ) -> str:
        """
        Retrieve representative project context.
        """

        retriever = self._get_retriever(
            repository
        )

        docs = retriever.retrieve_project_context(
            k=k,
        )

        return "\n\n".join(
            f"""
    File:
    {item["metadata"]["path"]}

    {item["content"]}
    """
            for item in docs
        )

    def _get_file_context(
        self,
        repository: str,
        file_path: str,
    ) -> str:
        """
        Retrieve the complete context for a specific file.
        """

        retriever = self._get_retriever(
            repository
        )

        docs = retriever.retrieve_file_context(
            file_path
        )

        if not docs:
            return ""

        return "\n\n".join(
            f"""
    File:
    {item["metadata"]["path"]}

    {item["content"]}
    """
            for item in docs
        )

    def _get_repository_summary(
        self,
        repository: str,
    ) -> str:
        """
        Generate a formatted repository intelligence summary.
        """

        repository_intelligence = (
            self._repository_intelligence(
                repository
            )
        )

        return self._format_repository_intelligence(
            repository_intelligence
        )

    def _format_repository_intelligence(
        self,
        intelligence: dict,
    ) -> str:
        """
        Convert repository intelligence into Markdown.
        """

        terraform = intelligence["terraform"]
        kubernetes = intelligence["kubernetes"]
        docker = intelligence["docker"]
        helm = intelligence["helm"]
        github = intelligence["github_actions"]

        lines = [
            "# Repository Intelligence",
            "",
            "## Terraform",
            f"- Providers: {', '.join(terraform['providers']) or 'None'}",
            f"- Modules: {', '.join(terraform['modules']) or 'None'}",
            f"- Resources: {terraform['resource_count']}",
            f"- Variables: {terraform['variables']}",
            f"- Outputs: {terraform['outputs']}",
            "",
            "## Kubernetes",
            f"- Deployments: {', '.join(kubernetes['deployments']) or 'None'}",
            f"- Services: {', '.join(kubernetes['services']) or 'None'}",
            f"- ConfigMaps: {kubernetes['configmaps']}",
            f"- Secrets: {kubernetes['secrets']}",
            f"- PVCs: {kubernetes['persistent_volume_claims']}",
            f"- Jobs: {kubernetes['jobs']}",
            f"- YAML Files: {kubernetes['summary']['yaml_files']}",
            "",
            "## Docker",
        ]

        if docker["dockerfiles"]:
            for dockerfile in docker["dockerfiles"]:
                lines.extend(
                    [
                        f"- Dockerfile: {dockerfile['path']}",
                        f"  - Base Images: {', '.join(dockerfile['base_images'])}",
                        f"  - Stages: {dockerfile['stages']}",
                        f"  - Exposed Ports: {', '.join(map(str, dockerfile['exposed_ports'])) or 'None'}",
                    ]
                )
        else:
            lines.append("- No Dockerfiles found")

        lines.extend(
            [
                "",
                "## Helm",
                f"- Charts: {helm['summary']['charts']}",
                f"- Templates: {helm['summary']['templates']}",
                f"- Values Files: {helm['summary']['values_files']}",
                "",
                "## GitHub Actions",
            ]
        )

        if github["workflows"]:
            for workflow in github["workflows"]:
                lines.extend(
                    [
                        f"- Workflow: {workflow['name']}",
                        f"  - Jobs: {', '.join(workflow['jobs'])}",
                        f"  - Triggers: {', '.join(workflow['triggers'])}",
                        f"  - Actions: {', '.join(workflow['actions'])}",
                    ]
                )
        else:
            lines.append("- No workflows found")

        return "\n".join(lines)

    def _build_project_overview_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the project overview endpoint.
        """

        return f"""
    You are an expert Software Architect and Senior DevOps Engineer.

    Analyze the repository below.

    Repository Intelligence
    ========================

    {repository_summary}

    Repository Context
    ==================

    {context}

    Generate a professional repository overview.

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Use Markdown headings (#, ##, ###).
    - Use bullet lists where appropriate.
    - Use Markdown tables if useful.
    - Do NOT wrap the response inside a JSON object.

    Include:

    # Executive Summary

    # Purpose

    # Tech Stack

    # Folder Structure

    # Main Components

    # Architecture

    # Data Flow

    # Security Observations

    # DevOps Observations

    # Improvements

    # Overall Rating (/10)
    """

    def _build_documentation_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the documentation endpoint.
        """

        return f"""
    You are a Senior Technical Writer.

    Generate professional documentation for this repository.

    Repository Intelligence
    ========================

    {repository_summary}

    Repository Context
    ==================

    {context}

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Use Markdown headings (#, ##, ###).
    - Use bullet lists.
    - Use Markdown tables when appropriate.

    Generate:

    # Project Overview

    # Features

    # Technology Stack

    # Folder Structure

    # Installation

    # Configuration

    # Environment Variables

    # API Overview

    # Deployment

    # CI/CD Pipeline

    # Future Improvements
    """

    def _build_performance_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the performance analysis endpoint.
        """

        return f"""
    You are a Senior Performance Engineer.

    Analyze this repository for performance improvements.

    Repository Intelligence
    ========================

    {repository_summary}

    Repository Context
    ==================

    {context}

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Use Markdown headings.

    Generate a report including:

    # Executive Summary

    # Expensive Operations

    # Memory Usage

    # Database Performance

    # API Performance

    # Frontend Performance

    # Backend Performance

    # Caching Opportunities

    # Algorithm Complexity

    # Optimization Recommendations

    # Performance Score (/10)
    """

    def _build_security_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the security analysis endpoint.
        """

        return f"""
    You are a Senior Application Security Engineer and DevSecOps Expert.

    Analyze the repository below.

    Repository Intelligence
    ========================

    {repository_summary}

    Repository Context
    ==================

    {context}

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Use Markdown headings and bullet lists.

    Include:

    # Executive Summary

    # Authentication & Authorization

    # Input Validation

    # Secrets & Credentials

    # Dependency Risks

    # Configuration Issues

    # Infrastructure Risks

    # Docker Security

    # Kubernetes Security

    # CI/CD Security

    # OWASP Top 10 Findings

    # Recommendations

    # Overall Security Score (/10)
    """

    def _build_code_review_prompt(
        self,
        repository: str,
        file_path: str,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the code review endpoint.
        """

        return f"""
    You are a Principal Software Engineer and Senior Code Reviewer.

    Review the following source file.

    Repository
    ==========

    {repository}

    Repository Intelligence
    ========================

    {repository_summary}

    File
    ====

    {file_path}

    Code
    ====

    {context}

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Use Markdown headings.
    - Use bullet lists where appropriate.

    Include:

    # Executive Summary

    # Correctness

    # Bugs & Potential Issues

    # Security Concerns

    # Performance

    # Readability

    # Maintainability

    # Best Practices

    # Refactoring Suggestions

    # Positive Aspects

    # Overall Rating (/10)
    """

    def _build_architecture_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the architecture endpoint.
        """

        return f"""

    You are a Principal Software Architect.

    Analyze the repository using ONLY the context below.

    Repository Intelligence
    ========================

    {repository_summary}

    Repository Context
    ==================

    {context}

    Generate the following response.

    ## Architecture

    Explain the architecture in the following sections:

    1. Infrastructure Layer
    2. CI/CD Layer
    3. Kubernetes Layer
    4. Monitoring Layer
    5. Security Layer
    6. Application Layer

    Use ONLY information found in the repository context.

    ## Mermaid

    Return ONE valid Mermaid flowchart wrapped in a fenced markdown code block.

    Example:

    ```mermaid
    graph TD
    User -->|HTTPS| NGINX_Ingress
    NGINX_Ingress --> React_Frontend
    React_Frontend --> NodeJS_Backend
    NodeJS_Backend --> MongoDB
    ```

    IMPORTANT MERMAID RULES:

    - Output ONLY a valid Mermaid flowchart.
    - Every connection MUST use this exact syntax:

    Source --> Destination

    or

    Source -->|Label| Destination

    - NEVER generate:

    Source -->|Label|> Destination

    - NEVER put a '>' after the label.
    - Node IDs must contain only letters, numbers and underscores.
    - Example:

    graph TD
    User -->|HTTPS| NGINX_Ingress
    NGINX_Ingress --> React_Frontend
    React_Frontend --> NodeJS_Backend
    NodeJS_Backend --> MongoDB

    Return exactly one Mermaid code block.

    Rules:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Explain the architecture first.
    - Then include ONE Mermaid diagram.
    - Do not invent technologies.
    - Base everything only on repository context.
    - Prefer README.md if it contains architecture information.
    - Use Terraform modules to identify infrastructure.
    - Use GitHub Actions workflows to identify CI/CD.
    - Use Kubernetes manifests and Helm charts to identify deployed services.
    - Include AWS services only if they are present in the repository.
    - Include monitoring components only if they exist in the repository.
    - The Mermaid diagram should represent the actual deployment architecture, not a generic flowchart.
    - Do not omit important components like EKS, ECR, GitHub Actions, Terraform, React, Node.js, MongoDB, Prometheus, Grafana, NGINX Ingress, AWS Load Balancer Controller, or cert-manager if they are present in the repository.

    """

    def _build_repository_health_prompt(
        self,
        context: str,
        repository_summary: str,
    ) -> str:
        """
        Build the prompt for the repository health endpoint.
        """

        return f"""

        You are a Senior Software Architect.

        Analyze this repository.

        Repository Intelligence
        ========================

        {repository_summary}

        Repository Context
        ==================

        {context}

        Return ONLY valid JSON.

        {{
        "overall_score": 0,
        "architecture": 0,
        "security": 0,
        "performance": 0,
        "documentation": 0,
        "code_quality": 0,
        "summary": "",
        "recommendations": [
            "",
            "",
            ""
        ]
        }}

    """

    def project_overview(
        self,
        repository: str,
    ):
        """
        Generate a high-level overview of the repository.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["overview"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_project_overview_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        return ask_groq(prompt)

    def generate_architecture(
        self,
        repository: str,
    ):

        """
        Generate an architecture explanation and Mermaid diagram.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["architecture"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_architecture_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        answer = ask_groq(prompt)

        # Fix common Mermaid mistakes produced by LLMs
        answer = re.sub(
            r'-->\|([^|]+)\|>',
            r'-->|\\1| ',
            answer,
        )

        logger.debug("Architecture analysis completed successfully.")

        return answer

    def generate_repository_map(
        self,
        repository_name: str,
    ):

        """
        Generate repository facts and an AI-assisted project summary.
        """
        repository_path = (
            self.DATA_DIR / repository_name
        )

        if not repository_path.exists():
            raise FileNotFoundError(
                "Repository not found."
            )

        scanner = RepositoryScanner(
            repository_path
        )

        repo = scanner.scan()

        facts_markdown = MarkdownFormatter(
            repo
        ).repository_map()

        logger.debug(
            "Repository scan completed: %d files, %d directories",
            repo["stats"]["total_files"],
            repo["stats"]["total_directories"],
        )

        prompt = f"""
    You are a Senior Software Architect.

    The user can already see the Repository Facts below.

    {facts_markdown}

    Do NOT repeat any information already shown in the Repository Facts, including:

    - File counts
    - Directory counts
    - Languages
    - Technology stack
    - Terraform providers
    - Terraform modules

    Instead, use those facts to provide insight.

    Return ONLY the following sections.

    # 📝 Repository Summary

    Explain:
    - What this project does
    - What kind of application it is
    - The overall architecture

    (3–5 paragraphs)

    ---

    # 📂 Folder Overview

    Explain the responsibility of the important folders.

    Focus on:

    - backend
    - frontend
    - terraform
    - helm
    - docker
    - docs
    - .github
    - any important project-specific folders

    Explain how they work together.

    ---

    # 🧭 Suggested Navigation

    If a new developer joins the project today, what files and folders should they read first?

    Give a recommended learning path.

    ---

    # 🚀 Development Workflow

    Explain the normal workflow for contributing to this repository.

    Include things like:

    - infrastructure
    - application
    - deployments
    - CI/CD
    - testing
    - documentation

    Keep the answer concise.

    Do NOT create tables.

    Do NOT repeat Repository Facts.
    """
        summary = ask_groq(prompt)

        return {
            "facts": repo,
            "facts_markdown": facts_markdown,
            "summary": summary,
        }

    def generate_dependency_graph(
        self,
        repository_name: str,
    ):

        """
        Generate a dependency graph and architectural analysis.
        """
        repository_path = (
            self.DATA_DIR / repository_name
        )

        if not repository_path.exists():
            raise FileNotFoundError(
                "Repository not found."
            )

        analyzer = DependencyAnalyzer(
            repository_path
        )

        edges = analyzer.analyze()

        def node_id(name: str):
            return re.sub(
                r"[^A-Za-z0-9_]",
                "_",
                name,
            )

        def group(node: str):
            node = node.lower()

            # Frontend
            if node.endswith((".js", ".jsx", ".ts", ".tsx")):
                if (
                    "frontend" in node
                    or "/src/" in node
                    or node.startswith("src/")
                ):
                    return "Frontend"
                return "JavaScript"

            # Backend
            if node.endswith(".py"):
                return "Backend"

            # Providers
            if node.startswith("provider:"):
                return "Providers"

            # Terraform module names
            terraform_modules = {
                "vpc",
                "eks",
                "ecr",
                "alb",
                "ingress",
                "monitoring",
                "metrics",
                "cert-manager",
                "github-oidc",
                "iam",
                "network",
            }

            if node in terraform_modules:
                return "Terraform Modules"

            # Terraform files
            if node.endswith(".tf"):
                return "Terraform"

            # Terraform module paths (backward compatibility)
            if (
                "./modules/" in node
                or "../modules/" in node
                or "modules/" in node
            ):
                return "Terraform Modules"

            # GitHub Actions
            if ".github/workflows" in node:
                return "GitHub Actions"

            # Kubernetes / Helm
            if node.endswith((".yaml", ".yml")):
                return "Kubernetes"

            return "Other"

        groups = defaultdict(set)
        relationships = []

        for source, target in edges:

            source = (
                source.replace("\\", "/")
                .replace('"', "")
            )

            target = (
                target.replace("\\", "/")
                .replace('"', "")
            )

            groups[group(source)].add(source)
            groups[group(target)].add(target)

            relationships.append(
                (source, target)
            )

        mermaid = ["graph LR"]

        declared = {}

        for group_name in sorted(groups):

            mermaid.append(
                f"subgraph {node_id(group_name)}[{group_name}]"
            )

            for node in sorted(groups[group_name]):

                nid = node_id(node)
                declared[node] = nid

                mermaid.append(
                    f'    {nid}["{node}"]'
                )

            mermaid.append("end")
            mermaid.append("")

        for source, target in relationships:

            mermaid.append(
                f"{declared[source]} --> {declared[target]}"
            )

        mermaid_graph = "\n".join(
            mermaid
        )

        prompt = f"""
    You are a Principal Software Architect.

    Below is a dependency graph extracted from a repository.

    Analyze this dependency graph.

    Dependency Graph

    {mermaid_graph}

    Provide:

    # Dependency Analysis

    - Core Modules
    - High Coupling
    - Layering
    - Design Quality
    - Suggested Improvements

    IMPORTANT:

    - Return GitHub-Flavored Markdown.
    - Do NOT return JSON.
    - Do NOT regenerate the Mermaid diagram.
    - Only provide the analysis.
    """

        analysis = ask_groq(prompt)

        return {
            "analysis": analysis,
            "mermaid": mermaid_graph,
        }


    def security_analysis(
        self,
        repository: str,
    ):

        """
        Analyze the repository for security risks and best practices.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["security"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_security_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        return ask_groq(prompt)

    def code_review(
        self,
        repository: str,
        file_path: str,
    ):

        """
        Review a specific source file using AI.
        """
        context = self._get_file_context(
            repository,
            file_path,
        )

        if not context:
            return f"No code found for '{file_path}'."

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_code_review_prompt(
            repository=repository,
            file_path=file_path,
            context=context,
            repository_summary=repository_summary,
        )

        return ask_groq(prompt)

    def performance_analysis(
        self,
        repository: str,
    ):

        """
        Analyze the repository for performance improvements.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["performance"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_performance_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        return ask_groq(prompt)

    def generate_documentation(
        self,
        repository: str,
    ):

        """
        Generate project documentation from repository context.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["documentation"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_documentation_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        return ask_groq(prompt)

    def repository_health(
        self,
        repository: str,
    ):

        """
        Generate repository health metrics and recommendations.
        """
        context = self._get_project_context(
            repository,
            RAG_CONTEXT["repository_health"],
        )

        repository_summary = self._get_repository_summary(
            repository
        )

        prompt = self._build_repository_health_prompt(
            context=context,
            repository_summary=repository_summary,
        )

        answer = ask_groq(
            prompt,
            json_mode=True,
        )

        logger.debug(
            "Repository health analysis completed."
        )

        match = re.search(r"\{.*\}", answer, re.DOTALL)

        if not match:
            raise ValueError(
                f"No JSON found in response:\n{answer}"
            )

        return json.loads(match.group(0))