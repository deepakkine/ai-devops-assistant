from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Files"])


@router.get("/files/{repository}")
def list_files(repository: str):

    repo_path = Path("../data") / repository

    if not repo_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Repository not found.",
        )

    files = []

    for path in repo_path.rglob("*"):

        if not path.is_file():
            continue

        if ".git" in path.parts:
            continue

        files.append(
            str(path.relative_to(repo_path))
        )

    return sorted(files)


@router.get("/file/{repository}")
def get_file(repository: str, path: str):

    repo_path = Path("../data") / repository

    file_path = repo_path / path

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail="Invalid file.",
        )

    try:

        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return {
        "path": path,
        "content": content,
    }