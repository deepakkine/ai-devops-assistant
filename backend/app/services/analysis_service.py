import re
from pathlib import Path

from app.core.gemini_client import ask_gemini
from app.rag.retriever import Retriever
from app.services.dependency_analyzer import (
    DependencyAnalyzer,
)


class AnalysisService:

    DATA_DIR = Path("../data")

    def project_overview(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context()

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are an expert Software Architect and Senior DevOps Engineer.

Analyze the repository below.

Repository Context
==================

{context}

Generate a professional repository overview.

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

        return ask_gemini(prompt)

    def generate_architecture(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(
            k=40,
        )

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are a Principal Software Architect.

Analyze the repository using ONLY the context below.

Repository Context
==================

{context}

Generate the following response.

## Architecture

Explain the architecture of the repository.

## Mermaid

Return ONLY ONE Mermaid diagram.

Example:

graph TD
User --> Frontend
Frontend --> Backend
Backend --> Database

Rules:

- Do not invent technologies.
- Base everything only on repository context.
"""

        return ask_gemini(prompt)

    def generate_repository_map(
        self,
        repository_name: str,
    ):
        repository_path = (
            self.DATA_DIR / repository_name
        )

        if not repository_path.exists():
            raise FileNotFoundError(
                "Repository not found."
            )

        tree = []

        for path in sorted(
            repository_path.rglob("*")
        ):
            relative = path.relative_to(
                repository_path
            )

            if ".git" in relative.parts:
                continue

            indent = "  " * (
                len(relative.parts) - 1
            )

            prefix = (
                "📁"
                if path.is_dir()
                else "📄"
            )

            tree.append(
                f"{indent}{prefix} {relative.name}"
            )

        prompt = f"""
You are a Principal Software Architect.

Repository Structure
====================

{chr(10).join(tree)}

Generate:

# Repository Summary

# Module Map

# Folder Relationships

# Suggested Navigation
"""

        return ask_gemini(prompt)

    def generate_dependency_graph(
        self,
        repository_name: str,
    ):
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

        mermaid = [
            "graph TD"
        ]

        declared = set()

        def node_id(name: str):
            return re.sub(
                r"[^A-Za-z0-9_]",
                "_",
                name,
            )

        for source, target in edges:

            source = (
                source.replace("\\", "/")
                .replace('"', "")
            )

            target = (
                target.replace("\\", "/")
                .replace('"', "")
            )

            source_id = node_id(source)
            target_id = node_id(target)

            if source_id not in declared:
                mermaid.append(
                    f'{source_id}["{source}"]'
                )
                declared.add(source_id)

            if target_id not in declared:
                mermaid.append(
                    f'{target_id}["{target}"]'
                )
                declared.add(target_id)

            mermaid.append(
                f"{source_id} --> {target_id}"
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

- Core modules
- High coupling
- Layering
- Design quality
- Suggested improvements

Do NOT regenerate the Mermaid diagram.
Only provide the analysis.
"""

        analysis = ask_gemini(prompt)

        return {
            "analysis": analysis,
            "mermaid": mermaid_graph,
        }
    

    def security_analysis(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(
            k=40,
        )

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are a Senior Application Security Engineer and DevSecOps Expert.

Analyze the repository below.

Repository Context
==================

{context}

Generate a professional security report.

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

        return ask_gemini(prompt)
    
    def code_review(
        self,
        repository: str,
        file_path: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_file_context(file_path)

        if not docs:
            return f"No code found for '{file_path}'."

        context = "\n\n".join(
            f"""
File:
{item["metadata"]["path"]}

{item["content"]}
"""
            for item in docs
        )

        prompt = f"""
You are a Principal Software Engineer and Senior Code Reviewer.

Review the following source file.

Repository
==========

{repository}

File
====

{file_path}

Code
====

{context}

Generate a detailed professional code review.

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

        return ask_gemini(prompt)
    
    def performance_analysis(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(k=40)

        context = "\n\n".join(
            f"""
    File:
    {item["metadata"]["path"]}

    {item["content"]}
    """
            for item in docs
        )

        prompt = f"""
    You are a Senior Performance Engineer.

    Analyze this repository for performance improvements.

    Repository
    ==========

    {context}

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

        return ask_gemini(prompt)
    
    def generate_documentation(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(k=40)

        context = "\n\n".join(
            f"""
    File:
    {item["metadata"]["path"]}

    {item["content"]}
    """
            for item in docs
        )

        prompt = f"""
    You are a Senior Technical Writer.

    Generate professional documentation for this repository.

    Repository
    ==========

    {context}

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

        return ask_gemini(prompt)
    
    def repository_health(
        self,
        repository: str,
    ):
        retriever = Retriever(repository)

        docs = retriever.retrieve_project_context(k=40)

        context = "\n\n".join(
            f"""
    File:
    {item["metadata"]["path"]}

    {item["content"]}
    """
            for item in docs
        )

        prompt = f"""
    You are a Senior Software Architect.

    Analyze this repository.

    Repository
    ==========

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

        answer = ask_gemini(prompt)

        import json

        return json.loads(answer)