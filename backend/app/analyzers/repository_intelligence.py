"""Repository Intelligence Aggregator."""

import logging
from pathlib import Path
from typing import Any

from app.analyzers.docker_analyzer import DockerAnalyzer
from app.analyzers.github_actions_analyzer import (
    GitHubActionsAnalyzer,
)
from app.analyzers.helm_analyzer import HelmAnalyzer
from app.analyzers.kubernetes_analyzer import (
    KubernetesAnalyzer,
)
from app.analyzers.terraform_analyzer import (
    TerraformAnalyzer,
)

logger = logging.getLogger(__name__)


class RepositoryIntelligence:
    """Aggregate repository intelligence from multiple analyzers."""

    def __init__(self, repository_path: Path):
        """Initialize the repository intelligence analyzer."""
        self.repository_path = repository_path

    def analyze(self) -> dict[str, Any]:
        """Analyze the repository."""

        logger.info(
            "Starting repository intelligence analysis for %s",
            self.repository_path,
        )

        analyzers = {
            "terraform": TerraformAnalyzer(
                self.repository_path
            ),
            "kubernetes": KubernetesAnalyzer(
                self.repository_path
            ),
            "docker": DockerAnalyzer(
                self.repository_path
            ),
            "helm": HelmAnalyzer(
                self.repository_path
            ),
            "github_actions": GitHubActionsAnalyzer(
                self.repository_path
            ),
        }

        results: dict[str, Any] = {}

        for name, analyzer in analyzers.items():
            try:
                logger.info(
                    "Running %s analyzer",
                    name,
                )

                results[name] = analyzer.analyze()

            except Exception:
                logger.exception(
                    "Failed running %s analyzer",
                    name,
                )

                results[name] = {
                    "error": (
                        f"{name} analyzer failed"
                    )
                }

        results["summary"] = {
            "has_terraform": bool(
                results.get("terraform", {}).get(
                    "resource_count", 0
                )
            ),
            "has_kubernetes": bool(
                results.get("kubernetes", {})
                .get("summary", {})
                .get("resources", 0)
            ),
            "has_docker": bool(
                results.get("docker", {})
                .get("summary", {})
                .get("dockerfiles", 0)
            ),
            "has_helm": bool(
                results.get("helm", {})
                .get("summary", {})
                .get("charts", 0)
            ),
            "has_github_actions": bool(
                results.get("github_actions", {})
                .get("summary", {})
                .get("workflows", 0)
            ),
            "technologies": {
                "terraform": results.get(
                    "terraform", {}
                ).get(
                    "resource_count",
                    0,
                ),
                "kubernetes": results.get(
                    "kubernetes", {}
                ).get(
                    "summary", {}
                ).get(
                    "resources",
                    0,
                ),
                "docker": results.get(
                    "docker", {}
                ).get(
                    "summary", {}
                ).get(
                    "dockerfiles",
                    0,
                ),
                "helm": results.get(
                    "helm", {}
                ).get(
                    "summary", {}
                ).get(
                    "charts",
                    0,
                ),
                "github_actions": results.get(
                    "github_actions", {}
                ).get(
                    "summary", {}
                ).get(
                    "workflows",
                    0,
                ),
            },
        }

        logger.info(
            (
                "Repository intelligence analysis completed. "
                "Terraform=%s Kubernetes=%s Docker=%s "
                "Helm=%s GitHubActions=%s"
            ),
            results["summary"][
                "has_terraform"
            ],
            results["summary"][
                "has_kubernetes"
            ],
            results["summary"][
                "has_docker"
            ],
            results["summary"][
                "has_helm"
            ],
            results["summary"][
                "has_github_actions"
            ],
        )

        return results