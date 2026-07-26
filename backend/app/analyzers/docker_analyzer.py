"""Analyzer for Dockerfiles."""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DockerAnalyzer:
    """Analyze Dockerfiles in a repository."""

    def __init__(self, repository_path: Path):
        """Initialize the analyzer."""
        self.repository_path = repository_path

    def analyze(self) -> dict[str, Any]:
        """Analyze Dockerfiles."""

        logger.info(
            "Starting Docker analysis for repository: %s",
            self.repository_path,
        )

        dockerfiles = []

        dockerfiles.extend(self.repository_path.rglob("Dockerfile"))
        dockerfiles.extend(self.repository_path.rglob("Dockerfile.*"))

        logger.info(
            "Discovered %d Dockerfiles.",
            len(dockerfiles),
        )

        dockerfile_details: list[dict[str, Any]] = []
        base_images: set[str] = set()

        multi_stage_builds = 0
        total_exposed_ports = 0

        for dockerfile in dockerfiles:
            try:
                with dockerfile.open("r", encoding="utf-8") as file:
                    lines = file.readlines()

                stages = 0
                base_images_in_file: list[str] = []
                workdir = None
                exposed_ports: list[int] = []
                cmd = None
                entrypoint = None
                user = None

                for line in lines:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    upper_line = line.upper()

                    if upper_line.startswith("FROM "):
                        stages += 1

                        image = line.split(maxsplit=1)[1]
                        image = image.split(" AS ")[0].split(" as ")[0].strip()

                        base_images_in_file.append(image)
                        base_images.add(image)

                    elif upper_line.startswith("WORKDIR "):
                        workdir = line.split(maxsplit=1)[1].strip()

                    elif upper_line.startswith("EXPOSE "):
                        ports = line.split(maxsplit=1)[1].split()

                        for port in ports:
                            try:
                                exposed_ports.append(int(port.split("/")[0]))
                            except ValueError:
                                continue

                    elif upper_line.startswith("CMD "):
                        cmd = line.split(maxsplit=1)[1].strip()

                    elif upper_line.startswith("ENTRYPOINT "):
                        entrypoint = line.split(maxsplit=1)[1].strip()

                    elif upper_line.startswith("USER "):
                        user = line.split(maxsplit=1)[1].strip()

                if stages > 1:
                    multi_stage_builds += 1

                total_exposed_ports += len(exposed_ports)

                dockerfile_details.append(
                    {
                        "path": str(
                            dockerfile.relative_to(self.repository_path)
                        ),
                        "base_images": base_images_in_file,
                        "stages": stages,
                        "workdir": workdir,
                        "exposed_ports": exposed_ports,
                        "entrypoint": entrypoint,
                        "cmd": cmd,
                        "user": user,
                        "runs_as_non_root": (
                            user is not None and user.lower() != "root"
                        ),
                    }
                )

            except Exception as error:
                logger.warning(
                    "Failed to parse %s: %s",
                    dockerfile,
                    error,
                )

        logger.info(
            (
                "Docker analysis completed. "
                "Dockerfiles=%d, Base Images=%d, Multi-stage=%d"
            ),
            len(dockerfile_details),
            len(base_images),
            multi_stage_builds,
        )

        return {
            "dockerfiles": dockerfile_details,
            "summary": {
                "dockerfiles": len(dockerfile_details),
                "base_images": sorted(base_images),
                "base_image_count": len(base_images),
                "multi_stage_builds": multi_stage_builds,
                "total_exposed_ports": total_exposed_ports,
            },
        }