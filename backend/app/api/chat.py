from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

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
            selected_file=request.selected_file,
            history=request.history,
        )

        return ChatResponse(**response)

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.post("/chat/stream")
def stream_chat(request: ChatRequest):
    try:
        generator = chat_service.stream_chat(
            repository=request.repository,
            question=request.question,
            selected_file=request.selected_file,
            history=request.history,
        )

        return StreamingResponse(
            generator,
            media_type="text/plain",
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.get("/chat/project-overview/{repository}")
def project_overview(repository: str):
    try:
        answer = chat_service.project_overview(
            repository
        )

        return {
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.get("/chat/architecture/{repository}")
def architecture(repository: str):
    try:
        answer = chat_service.generate_architecture(
            repository
        )

        return {
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )