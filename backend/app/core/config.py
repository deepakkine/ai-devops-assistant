from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set."
    )

# =============================================================================
# RAG Configuration
# =============================================================================

RAG_CONTEXT = {
    "overview": 15,
    "architecture": 15,
    "repository_health": 15,
    "documentation": 15,
    "security": 25,
    "performance": 25,
    "qa": 5,
}

# =============================================================================
# Text Splitting
# =============================================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# =============================================================================
# Embedding Model
# =============================================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# =============================================================================
# LLM Models
# =============================================================================

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
FALLBACK_GROQ_MODEL = "llama-3.1-8b-instant"

# =============================================================================
# ChromaDB
# =============================================================================

CHROMADB_PATH = "./storage/chromadb"