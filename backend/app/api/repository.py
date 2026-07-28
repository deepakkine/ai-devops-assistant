import traceback
from chromadb import PersistentClient
from fastapi import APIRouter, HTTPException

from app.schemas.repository import (
    RepositoryImportRequest,
    RepositoryImportResponse,
)
from app.services.analysis_service import AnalysisService
from app.services.repository_service import RepositoryService

router = APIRouter(tags=["Repositories"])

repository_service = RepositoryService()
analysis_service = AnalysisService()


@router.post(
    "/repositories/import",
    response_model=RepositoryImportResponse,
)
async def import_repository(request: RepositoryImportRequest):
    try:
        repo = repository_service.clone(
            request.github_url
        )

        return RepositoryImportResponse(
            message="Repository cloned successfully.",
            repository_name=repo,
        )

    except Exception:
        print("=" * 80)
        print("IMPORT ENDPOINT FAILED")
        traceback.print_exc()
        print("=" * 80)
        raise


@router.get("/repositories")
def list_repositories():
    client = PersistentClient(
        path="./storage/chromadb"
    )

    return sorted(
        [
            collection.name
            for collection in client.list_collections()
        ]
    )


@router.get("/repositories/{repository_name}/map")
def repository_map(repository_name: str):
    try:
        return analysis_service.generate_repository_map(
                repository_name
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.delete("/repositories/{repository_name}")
def delete_repository(repository_name: str):
    try:
        return repository_service.delete(
            repository_name
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )