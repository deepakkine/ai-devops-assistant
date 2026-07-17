import re
from pathlib import Path


IGNORE_IMPORTS = {
    "react",
    "react-dom",
    "axios",
    "fastapi",
    "chromadb",
    "pathlib",
    "subprocess",
    "shutil",
}


class DependencyAnalyzer:

    def __init__(self, repository_path: Path):
        self.repository_path = repository_path

    def analyze(self):
        edges = set()

        for file in self.repository_path.rglob("*"):

            if not file.is_file():
                continue

            if ".git" in file.parts:
                continue

            suffix = file.suffix.lower()

            if suffix in {
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
            }:
                edges.update(
                    self._analyze_js(file)
                )

            elif suffix == ".py":
                edges.update(
                    self._analyze_python(file)
                )

            elif suffix == ".tf":
                edges.update(
                    self._analyze_terraform(file)
                )

        return sorted(edges)

    def _source(self, file: Path):
        return file.relative_to(
            self.repository_path
        ).as_posix()

    def _analyze_js(self, file: Path):
        text = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        imports = re.findall(
            r'import.*?from\s+[\'"](.+?)[\'"]',
            text,
        )

        imports += re.findall(
            r'import\s+[\'"](.+?)[\'"]',
            text,
        )

        edges = set()

        source = self._source(file)

        for target in imports:

            if target.startswith("."):
                edges.add(
                    (
                        source,
                        target,
                    )
                )

        return edges

    def _analyze_python(self, file: Path):
        text = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        imports = re.findall(
            r"^import\s+(.+)$",
            text,
            re.MULTILINE,
        )

        imports += re.findall(
            r"^from\s+(.+?)\s+import",
            text,
            re.MULTILINE,
        )

        edges = set()

        source = self._source(file)

        for target in imports:

            module = target.split(".")[0]

            if module in IGNORE_IMPORTS:
                continue

            edges.add(
                (
                    source,
                    target,
                )
            )

        return edges

    def _analyze_terraform(
        self,
        file: Path,
    ):
        text = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        modules = re.findall(
            r'source\s*=\s*"(.+?)"',
            text,
        )

        edges = set()

        source = self._source(file)

        for module in modules:

            edges.add(
                (
                    source,
                    module,
                )
            )

        return edges