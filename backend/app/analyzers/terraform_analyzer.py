import logging
import re
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)


class TerraformAnalyzer:
    """
    Analyze Terraform configuration files and extract
    repository intelligence.
    """

    def __init__(self, repository_path: Path):
        self.repository_path = Path(repository_path)

    def analyze(self) -> dict:
        """
        Scan all Terraform files in the repository and
        extract providers, modules, resources, variables,
        and outputs.
        """

        providers = set()
        modules = set()
        resources = Counter()

        variable_count = 0
        output_count = 0

        terraform_files = list(
            self.repository_path.rglob("*.tf")
        )

        logger.info(
            "Found %d Terraform files.",
            len(terraform_files),
        )

        for tf_file in terraform_files:
            logger.debug(
                "Analyzing Terraform file: %s",
                tf_file,
            )

            try:
                content = tf_file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                logger.exception(
                    "Failed to read Terraform file: %s",
                    tf_file,
                )
                continue

            # Providers
            providers.update(
                re.findall(
                    r'provider\s+"([^"]+)"',
                    content,
                )
            )

            # Modules
            modules.update(
                re.findall(
                    r'module\s+"([^"]+)"',
                    content,
                )
            )

            # Resources
            for resource_type in re.findall(
                r'resource\s+"([^"]+)"\s+"[^"]+"',
                content,
            ):
                resources[resource_type] += 1

            # Variables
            variable_count += len(
                re.findall(
                    r'variable\s+"[^"]+"',
                    content,
                )
            )

            # Outputs
            output_count += len(
                re.findall(
                    r'output\s+"[^"]+"',
                    content,
                )
            )

        logger.info(
            (
                "Terraform analysis completed. "
                "Files=%d, Providers=%d, Modules=%d, Resources=%d"
            ),
            len(terraform_files),
            len(providers),
            len(modules),
            sum(resources.values()),
        )

        return {
            "providers": sorted(providers),
            "provider_count": len(providers),

            "modules": sorted(modules),
            "module_count": len(modules),

            "resources": dict(resources),
            "resource_count": sum(resources.values()),

            "variables": variable_count,
            "outputs": output_count,

            "terraform_file_count": len(terraform_files),
        }