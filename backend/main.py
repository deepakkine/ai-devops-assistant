from fastapi import FastAPI
from pydantic import BaseModel

from app.services.chat_service import ChatService

app = FastAPI(
    title="AI DevOps Assistant",
    description="AI-powered DevOps Assistant API",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "status": "running",
        "application": "AI DevOps Assistant",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ChatService.chat(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }