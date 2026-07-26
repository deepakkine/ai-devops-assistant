"""Analyzer for Kubernetes manifests."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class KubernetesAnalyzer:
    """Analyze Kubernetes manifests in a repository."""

    def __init__(self, repository_path: Path):
        """Initialize the analyzer."""
        self.repository_path = repository_path

    def analyze(self) -> dict[str, Any]:
        """Analyze Kubernetes YAML manifests."""
        logger.info(
            "Starting Kubernetes analysis for repository: %s",
            self.repository_path,
        )

        yaml_files = list(self.repository_path.rglob("*.yaml"))
        yaml_files.extend(self.repository_path.rglob("*.yml"))

        logger.info(
            "Discovered %d YAML files.",
            len(yaml_files),
        )

        resource_lists: dict[str, list[str]] = {
            "Deployment": [],
            "StatefulSet": [],
            "DaemonSet": [],
            "Service": [],
            "Ingress": [],
        }

        resource_counters: dict[str, int] = {
            "ConfigMap": 0,
            "Secret": 0,
            "PersistentVolume": 0,
            "PersistentVolumeClaim": 0,
            "HorizontalPodAutoscaler": 0,
            "Job": 0,
            "CronJob": 0,
            "ServiceAccount": 0,
            "Role": 0,
            "RoleBinding": 0,
            "ClusterRole": 0,
            "ClusterRoleBinding": 0,
        }

        resource_count = 0

        for yaml_file in yaml_files:
            try:
                with yaml_file.open("r", encoding="utf-8") as file:
                    documents = yaml.safe_load_all(file)

                    for document in documents:
                        if not isinstance(document, dict):
                            continue

                        kind = document.get("kind")
                        if not kind:
                            continue

                        resource_count += 1

                        metadata = document.get("metadata", {})
                        name = metadata.get("name", "unknown")

                        if kind in resource_lists:
                            resource_lists[kind].append(name)

                        elif kind in resource_counters:
                            resource_counters[kind] += 1

            except Exception as error:
                logger.warning(
                    "Failed to parse %s: %s",
                    yaml_file,
                    error,
                )

        logger.info(
            (
                "Kubernetes analysis completed. "
                "YAML Files=%d, Resources=%d, Deployments=%d, Services=%d"
            ),
            len(yaml_files),
            resource_count,
            len(resource_lists["Deployment"]),
            len(resource_lists["Service"]),
        )

        return {
            "deployments": resource_lists["Deployment"],
            "statefulsets": resource_lists["StatefulSet"],
            "daemonsets": resource_lists["DaemonSet"],
            "services": resource_lists["Service"],
            "ingresses": resource_lists["Ingress"],
            "configmaps": resource_counters["ConfigMap"],
            "secrets": resource_counters["Secret"],
            "persistent_volumes": resource_counters["PersistentVolume"],
            "persistent_volume_claims": resource_counters["PersistentVolumeClaim"],
            "horizontal_pod_autoscalers": resource_counters[
                "HorizontalPodAutoscaler"
            ],
            "jobs": resource_counters["Job"],
            "cronjobs": resource_counters["CronJob"],
            "service_accounts": resource_counters["ServiceAccount"],
            "roles": resource_counters["Role"],
            "role_bindings": resource_counters["RoleBinding"],
            "cluster_roles": resource_counters["ClusterRole"],
            "cluster_role_bindings": resource_counters["ClusterRoleBinding"],
            "summary": {
                "yaml_files": len(yaml_files),
                "resources": resource_count,
                "deployments": len(resource_lists["Deployment"]),
                "statefulsets": len(resource_lists["StatefulSet"]),
                "daemonsets": len(resource_lists["DaemonSet"]),
                "services": len(resource_lists["Service"]),
                "ingresses": len(resource_lists["Ingress"]),
                "configmaps": resource_counters["ConfigMap"],
                "secrets": resource_counters["Secret"],
                "persistent_volumes": resource_counters["PersistentVolume"],
                "persistent_volume_claims": resource_counters[
                    "PersistentVolumeClaim"
                ],
                "horizontal_pod_autoscalers": resource_counters[
                    "HorizontalPodAutoscaler"
                ],
                "jobs": resource_counters["Job"],
                "cronjobs": resource_counters["CronJob"],
                "service_accounts": resource_counters["ServiceAccount"],
                "roles": resource_counters["Role"],
                "role_bindings": resource_counters["RoleBinding"],
                "cluster_roles": resource_counters["ClusterRole"],
                "cluster_role_bindings": resource_counters[
                    "ClusterRoleBinding"
                ],
            },
        }