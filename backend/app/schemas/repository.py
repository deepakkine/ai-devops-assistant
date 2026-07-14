from pydantic import BaseModel


class RepositoryImportRequest(BaseModel):
    github_url: str


class RepositoryImportResponse(BaseModel):
    message: str
    repository_name: str