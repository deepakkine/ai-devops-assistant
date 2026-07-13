from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".md",
    ".tf",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".js",
}

SUPPORTED_FILENAMES = {
    "Dockerfile",
    "Makefile",
}

IGNORE_DIRECTORIES = {
    ".git",
    ".terraform",
    "node_modules",
    "__pycache__",
    "venv",
}


class DocumentLoader:

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def load_documents(self):

        documents = []

        for path in self.repo_path.rglob("*"):

            if path.is_dir():
                continue

            if any(part in IGNORE_DIRECTORIES for part in path.parts):
                continue

            if (
                path.suffix not in SUPPORTED_EXTENSIONS
                and path.name not in SUPPORTED_FILENAMES
            ):
                continue

            try:

                text = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                documents.append(
                    {
                        "path": str(path.relative_to(self.repo_path)),
                        "content": text,
                        "extension": path.suffix,
                    }
                )

            except Exception:

                pass

        return documents