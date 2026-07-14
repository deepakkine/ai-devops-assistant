from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.repository import router as repository_router

app = FastAPI(
    title="AI DevOps Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")
app.include_router(repository_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "AI DevOps Assistant API"}


@app.get("/health")
def health():
    return {"status": "healthy"}