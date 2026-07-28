class MarkdownFormatter:

    def __init__(self, repository):
        self.repo = repository

    def repository_map(self):
        return f"""
# 📦 Repository Facts

## Repository

Name:
{self.repo["name"]}

## 📊 Statistics

| Metric | Value |
|---------|------:|
| Files | {self.repo["stats"]["total_files"]} |
| Directories | {self.repo["stats"]["total_directories"]} |
| Languages | {self.repo["stats"]["languages"]} |

## 💻 Languages

{self._language_table()}

## 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Frontend | {self._join(self.repo["technologies"]["frontend"])} |
| Backend | {self._join(self.repo["technologies"]["backend"])} |
| Infrastructure | {self._join(self.repo["technologies"]["infrastructure"])} |

## ☁️ Terraform Providers

Providers:
{self._bullet(self.repo["terraform"]["providers"])}

## 📦 Terraform Modules
{self._bullet(self.repo["terraform"]["modules"])}

Terraform Files:
{self.repo["terraform"]["files"]}
"""

    def _join(self, values):
        return ", ".join(values) if values else "Not detected"

    def _bullet(self, values):
        if not values:
            return "- None"

        return "\n".join(
            f"- {value}"
            for value in values
        )

    def _language_table(self):

        if not self.repo["languages"]:
            return "Not detected"

        rows = [
            "| Language | Files |",
            "|----------|------:|",
        ]

        for language, count in self.repo["languages"].items():
            rows.append(
                f"| {language} | {count} |"
            )

        return "\n".join(rows)