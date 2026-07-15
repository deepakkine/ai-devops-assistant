from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class Source(BaseModel):
    path: str
    chunk_id: int


class ChatRequest(BaseModel):
    repository: str
    question: str
    selected_file: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = Field(default_factory=list)