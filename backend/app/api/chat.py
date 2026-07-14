from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["Chat"])

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        response = chat_service.chat(
            repository=request.repository,
            question=request.question,
            history=request.history,
        )

        return ChatResponse(**response)

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=str(e),
        )