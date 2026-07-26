"""Analyzer for GitHub Actions workflows."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class GitHubActionsAnalyzer:
    """Analyze GitHub Actions workflows in a repository."""

    def __init__(self, repository_path: Path):
        """Initialize the analyzer."""
        self.repository_path = repository_path

    def analyze(self) -> dict[str, Any]:
        """Analyze GitHub Actions workflows."""

        logger.info(
            "Starting GitHub Actions analysis for repository: %s",
            self.repository_path,
        )

        workflow_files = (
            list(
                self.repository_path.rglob(
                    ".github/workflows/*.yml"
                )
            )
            + list(
                self.repository_path.rglob(
                    ".github/workflows/*.yaml"
                )
            )
        )

        logger.info(
            "Discovered %d workflow files.",
            len(workflow_files),
        )

        workflows: list[dict[str, Any]] = []

        total_jobs = 0
        total_steps = 0

        actions_used: set[str] = set()
        security_tools: set[str] = set()
        deployment_targets: set[str] = set()

        language_actions = {
            "setup-python": "python",
            "setup-node": "node",
            "setup-java": "java",
            "setup-go": "go",
            "setup-dotnet": "dotnet",
        }

        security_keywords = {
            "trivy": "trivy",
            "sonarqube": "sonarqube",
            "codeql": "codeql",
            "snyk": "snyk",
            "semgrep": "semgrep",
        }

        deployment_keywords = {
            "configure-aws-credentials": "aws",
            "amazon-ecr": "aws",
            "eks": "aws",

            "kubectl": "kubernetes",
            "kubernetes": "kubernetes",

            "helm": "helm",

            "aks": "azure",
            "azure/login": "azure",

            "gke": "gcp",
            "google-github-actions": "gcp",
        }

        for workflow_file in workflow_files:
            try:
                with workflow_file.open(
                    "r",
                    encoding="utf-8",
                ) as file:
                    workflow = (
                        yaml.safe_load(file) or {}
                    )

                jobs = workflow.get("jobs", {})

                triggers = workflow.get("on")

                if triggers is None:
                    triggers = workflow.get(True, [])

                if isinstance(triggers, dict):
                    triggers = list(triggers.keys())

                elif isinstance(triggers, str):
                    triggers = [triggers]

                elif isinstance(triggers, list):
                    triggers = triggers

                else:
                    triggers = []

                workflow_jobs = list(jobs.keys())

                step_count = 0
                workflow_actions: set[str] = set()
                workflow_languages: set[str] = set()
                matrix_build = False

                for job in jobs.values():
                    if not isinstance(job, dict):
                        continue

                    strategy = job.get("strategy", {})

                    if (
                        isinstance(strategy, dict)
                        and "matrix" in strategy
                    ):
                        matrix_build = True

                    steps = job.get("steps", [])

                    if not isinstance(steps, list):
                        continue

                    step_count += len(steps)

                    for step in steps:
                        if not isinstance(step, dict):
                            continue

                        action = step.get("uses")

                        run_command = step.get("run", "").lower()

                        if "pip" in run_command or "python" in run_command:
                            workflow_languages.add("python")

                        if "npm" in run_command or "node" in run_command:
                            workflow_languages.add("node")

                        if "mvn" in run_command or "gradle" in run_command:
                            workflow_languages.add("java")

                        if "go " in run_command:
                            workflow_languages.add("go")

                        if "dotnet" in run_command:
                            workflow_languages.add("dotnet")

                        if not action:
                            continue

                        action_name = action.split("@")[0]

                        workflow_actions.add(action_name)
                        actions_used.add(action_name)

                        action_lower = action_name.lower()

                        for (
                            keyword,
                            language,
                        ) in language_actions.items():
                            if keyword in action_lower:
                                workflow_languages.add(
                                    language
                                )

                        for (
                            keyword,
                            tool,
                        ) in security_keywords.items():
                            if keyword in action_lower:
                                security_tools.add(tool)

                        for (
                            keyword,
                            target,
                        ) in deployment_keywords.items():
                            if keyword in action_lower:
                                deployment_targets.add(
                                    target
                                )

                total_jobs += len(workflow_jobs)
                total_steps += step_count

                workflows.append(
                    {
                        "name": workflow.get("name"),
                        "path": str(
                            workflow_file.relative_to(
                                self.repository_path
                            )
                        ),
                        "triggers": triggers,
                        "jobs": workflow_jobs,
                        "job_count": len(
                            workflow_jobs
                        ),
                        "step_count": step_count,
                        "actions": sorted(
                            workflow_actions
                        ),
                        "languages": sorted(
                            workflow_languages
                        ),
                        "matrix_build": matrix_build,
                    }
                )

            except Exception as error:
                logger.warning(
                    "Failed to analyze workflow %s: %s",
                    workflow_file,
                    error,
                )

        logger.info(
            (
                "GitHub Actions analysis completed. "
                "Workflows=%d Jobs=%d Steps=%d"
            ),
            len(workflows),
            total_jobs,
            total_steps,
        )

        return {
            "workflows": workflows,
            "summary": {
                "workflows": len(workflows),
                "jobs": total_jobs,
                "steps": total_steps,
                "actions": sorted(actions_used),
                "action_count": len(actions_used),
                "action_count": len(workflow_actions),
                "security_tools": sorted(
                    security_tools
                ),
                "deployment_targets": sorted(
                    deployment_targets
                ),
            },
        }