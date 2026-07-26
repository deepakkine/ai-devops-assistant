"""Analyzer for Helm charts."""

import logging
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class HelmAnalyzer:
    """Analyze Helm charts in a repository."""

    def __init__(self, repository_path: Path):
        """Initialize the analyzer."""
        self.repository_path = repository_path

    def analyze(self) -> dict[str, Any]:
        """Analyze Helm charts."""

        logger.info(
            "Starting Helm analysis for repository: %s",
            self.repository_path,
        )

        chart_files = (
            list(self.repository_path.rglob("Chart.yaml"))
            + list(self.repository_path.rglob("Chart.yml"))
        )

        logger.info(
            "Discovered %d Helm charts.",
            len(chart_files),
        )

        helm_charts: list[dict[str, Any]] = []

        total_templates = 0
        total_values_files = 0
        total_dependencies = 0
        total_hooks = 0
        total_crds = 0
        total_subcharts = 0

        for chart_file in chart_files:
            try:
                chart_dir = chart_file.parent

                with chart_file.open("r", encoding="utf-8") as file:
                    chart = yaml.safe_load(file) or {}

                templates_dir = chart_dir / "templates"

                template_files = []

                if templates_dir.exists():
                    template_files.extend(templates_dir.rglob("*.yaml"))
                    template_files.extend(templates_dir.rglob("*.yml"))

                values_files = list(chart_dir.glob("values*.yaml"))
                values_files.extend(chart_dir.glob("values*.yml"))

                dependencies = chart.get("dependencies", [])

                helpers = (
                    templates_dir / "_helpers.tpl"
                ).exists()

                hooks = 0

                for template in template_files:
                    try:
                        content = template.read_text(
                            encoding="utf-8"
                        )

                        if "helm.sh/hook" in content:
                            hooks += 1

                    except Exception as error:
                        logger.warning(
                            "Failed to read template %s: %s",
                            template,
                            error,
                        )

                crds_dir = chart_dir / "crds"

                crd_count = 0

                if crds_dir.exists():
                    crd_count += len(list(crds_dir.glob("*.yaml")))
                    crd_count += len(list(crds_dir.glob("*.yml")))

                subcharts_dir = chart_dir / "charts"

                subchart_count = 0

                if subcharts_dir.exists():
                    subchart_count = len(
                        [
                            item
                            for item in subcharts_dir.iterdir()
                            if item.is_dir()
                        ]
                    )

                total_templates += len(template_files)
                total_values_files += len(values_files)
                total_dependencies += len(dependencies)
                total_hooks += hooks
                total_crds += crd_count
                total_subcharts += subchart_count

                helm_charts.append(
                    {
                        "name": chart.get("name"),
                        "version": chart.get("version"),
                        "app_version": chart.get("appVersion"),
                        "description": chart.get("description"),
                        "path": str(
                            chart_dir.relative_to(
                                self.repository_path
                            )
                        ),
                        "templates": len(template_files),
                        "values_files": len(values_files),
                        "dependency_names": [
                            dependency.get("name")
                            for dependency in dependencies
                        ],
                        "helpers": helpers,
                        "hooks": hooks,
                        "crds": crd_count,
                        "subcharts": subchart_count,
                    }
                )

            except Exception as error:
                logger.warning(
                    "Failed to analyze Helm chart %s: %s",
                    chart_file,
                    error,
                )

        logger.info(
            (
                "Helm analysis completed. "
                "Charts=%d, Templates=%d, Values Files=%d"
            ),
            len(helm_charts),
            total_templates,
            total_values_files,
        )

        return {
            "charts": helm_charts,
            "summary": {
                "charts": len(helm_charts),
                "templates": total_templates,
                "values_files": total_values_files,
                "dependencies": total_dependencies,
                "hooks": total_hooks,
                "crds": total_crds,
                "subcharts": total_subcharts,
            },
        }