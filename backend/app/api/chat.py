from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.analysis_service import AnalysisService
from app.services.chat_service import ChatService

router = APIRouter(tags=["Chat"])

chat_service = ChatService()
analysis_service = AnalysisService()


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
        answer = analysis_service.project_overview(
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
        answer = (
            analysis_service.generate_architecture(
                repository
            )
        )

        return {
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )


@router.get("/chat/dependency-graph/{repository}")
def dependency_graph(repository: str):
    try:
        result = (
            analysis_service.generate_dependency_graph(
                repository
            )
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    
@router.get("/chat/security-analysis/{repository}")
def security_analysis(repository: str):
    try:
        answer = analysis_service.security_analysis(
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
    
@router.get("/chat/code-review/{repository}/{file_path:path}")
def code_review(
    repository: str,
    file_path: str,
):
    try:
        answer = analysis_service.code_review(
            repository,
            file_path,
        )

        return {
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    
@router.get("/chat/performance-analysis/{repository}")
def performance_analysis(repository: str):
    try:
        answer = analysis_service.performance_analysis(repository)

        return {
            "answer": answer,
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=str(e),
        )
    
@router.get("/chat/documentation/{repository}")
def generate_documentation(repository: str):
    try:
        answer = analysis_service.generate_documentation(
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
    
@router.get("/chat/repository-health/{repository}")
async def repository_health(repository: str):
    try:
        return analysis_service.repository_health(repository)
    except Exception:
        traceback.print_exc()
        raise