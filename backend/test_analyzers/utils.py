from pathlib import Path


def select_repository() -> Path:
    """Prompt the user to select a repository."""

    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "data"

    repositories = sorted(
        repo
        for repo in data_dir.iterdir()
        if repo.is_dir()
    )

    if not repositories:
        raise RuntimeError(
            f"No repositories found in {data_dir}"
        )

    print("\nAvailable repositories:\n")

    for index, repo in enumerate(
        repositories,
        start=1,
    ):
        print(f"{index}. {repo.name}")

    while True:
        try:
            choice = int(
                input("\nSelect repository: ")
            )

            if 1 <= choice <= len(repositories):
                return repositories[choice - 1]

            print("Invalid selection.")

        except ValueError:
            print("Please enter a number.")