from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["Chat"])

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:

        answer = chat_service.chat(request.question)

        return ChatResponse(answer=answer)

    except Exception as e:

        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    
    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )