from collections import Counter
from pathlib import Path
import re


class RepositoryScanner:
    """
    Scans a repository and extracts structured metadata that can be
    reused by Repository Map, Documentation, Architecture,
    Dependency Graph, and Repository Health.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".terraform",
        ".idea",
        ".vscode",
        "dist",
        "build",
        ".next",
        ".pytest_cache",
        ".mypy_cache",
    }

    def __init__(self, repository_path: Path):
        self.repository_path = repository_path

    def scan(self):
        data = {
            "name": self.repository_path.name,
            "directories": [],
            "files": [],
            "languages": Counter(),
            "terraform": {
                "files": 0,
                "modules": [],
                "providers": [],
            },
            "technologies": {
                "frontend": [],
                "backend": [],
                "infrastructure": [],
            },
            "stats": {},
        }

        self._scan_tree(data)
        self._scan_terraform(data)
        self._scan_technologies(data)
        self._build_stats(data)

        data["directories"].sort()
        data["files"].sort()
        data["languages"] = dict(
            sorted(data["languages"].items())
        )

        return data

    def _scan_tree(self, data):
        """
        Scan repository tree and detect file languages.
        """

        for path in self.repository_path.rglob("*"):

            if any(
                part in self.IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            relative = path.relative_to(
                self.repository_path
            ).as_posix()

            if path.is_dir():
                data["directories"].append(relative)
            else:
                data["files"].append(relative)

                self._detect_language(
                    path.suffix.lower(),
                    data["languages"],
                )

    def _detect_language(
        self,
        suffix,
        languages,
    ):
        """
        Detect programming language from file extension.
        """

        mapping = {
            ".py": "Python",
            ".js": "JavaScript",
            ".jsx": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript",
            ".tf": "Terraform",
            ".yaml": "YAML",
            ".yml": "YAML",
            ".json": "JSON",
            ".md": "Markdown",
            ".sh": "Shell",
            ".html": "HTML",
            ".css": "CSS",
            ".scss": "SCSS",
            ".sql": "SQL",
            ".xml": "XML",
            ".go": "Go",
            ".java": "Java",
        }

        language = mapping.get(suffix)

        if language:
            languages[language] += 1

    def _scan_terraform(self, data):
        """
        Detect Terraform modules and providers.
        """

        modules = set()
        providers = set()

        tf_files = list(
            self.repository_path.rglob("*.tf")
        )

        for tf in tf_files:

            if any(
                part in self.IGNORED_DIRECTORIES
                for part in tf.parts
            ):
                continue

            try:
                content = tf.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                continue

            modules.update(
                re.findall(
                    r'module\s+"([^"]+)"',
                    content,
                )
            )

            providers.update(
                re.findall(
                    r'provider\s+"([^"]+)"',
                    content,
                )
            )

        data["terraform"] = {
            "files": len(tf_files),
            "modules": sorted(modules),
            "providers": sorted(providers),
        }

    def _scan_technologies(self, data):
        """
        Detect technologies used in the repository.
        """

        frontend = set()
        backend = set()
        infrastructure = set()

        for file in data["files"]:

            lower = file.lower()

            # ---------------- Frontend ----------------

            if lower.endswith("package.json") and "frontend" in lower:

                frontend.add("Node.js")

                try:
                    content = (
                        self.repository_path / file
                    ).read_text(
                        encoding="utf-8",
                        errors="ignore",
                    ).lower()

                    if "react" in content:
                        frontend.add("React")

                    if "react-scripts" in content:
                        frontend.add("Create React App")

                    if "vite" in content:
                        frontend.add("Vite")

                    if "next" in content:
                        frontend.add("Next.js")

                    if "typescript" in content:
                        frontend.add("TypeScript")

                except Exception:
                    pass

            # ---------------- Backend ----------------

            if lower.endswith("package.json") and "backend" in lower:

                backend.add("Node.js")

                try:
                    content = (
                        self.repository_path / file
                    ).read_text(
                        encoding="utf-8",
                        errors="ignore",
                    ).lower()

                    if "express" in content:
                        backend.add("Express.js")

                    if "nestjs" in content:
                        backend.add("NestJS")

                    if "fastify" in content:
                        backend.add("Fastify")

                    if "koa" in content:
                        backend.add("Koa")

                    if "mongoose" in content:
                        backend.add("MongoDB")

                    if "prisma" in content:
                        backend.add("Prisma")

                    if "sequelize" in content:
                        backend.add("Sequelize")

                    if "typescript" in content:
                        backend.add("TypeScript")

                except Exception:
                    pass

            # ---------------- Infrastructure ----------------

            if lower.endswith("dockerfile"):
                infrastructure.add("Docker")

            if "docker-compose" in lower:
                infrastructure.add("Docker Compose")

            if lower.endswith(".tf"):
                infrastructure.add("Terraform")

            if lower.endswith("chart.yaml"):
                infrastructure.add("Helm")

            if ".github/workflows/" in lower:
                infrastructure.add("GitHub Actions")

            if any(
                keyword in lower
                for keyword in (
                    "deployment",
                    "service",
                    "ingress",
                    "statefulset",
                    "daemonset",
                    "kubernetes",
                    "k8s",
                )
            ):
                infrastructure.add("Kubernetes")

        data["technologies"] = {
            "frontend": sorted(frontend),
            "backend": sorted(backend),
            "infrastructure": sorted(infrastructure),
        }

    def _build_stats(self, data):
        """
        Build repository statistics.
        """

        data["stats"] = {
            "total_files": len(data["files"]),
            "total_directories": len(
                data["directories"]
            ),
            "languages": len(
                data["languages"]
            ),
        }