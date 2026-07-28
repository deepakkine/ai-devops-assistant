"""
Utility script to index a local Git repository into ChromaDB.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore


repo_path = "../data/aws-three-tier-devsecops-platform"
repo_name = Path(repo_path).name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger.info("Loading repository...")

loader = DocumentLoader(repo_path)

documents = loader.load_documents()

logger.info(
    "Loaded %d documents",
    len(documents),
)

logger.info("Splitting documents...")

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

logger.info(
    "Generated %d chunks",
    len(chunks),
)

logger.info(
    "Generating embeddings and storing in ChromaDB..."
)

store = VectorStore(repo_name)

store.index_chunks(chunks)

logger.info("Indexing completed successfully.")

logger.info(
    "Stored vectors: %d",
    store.count(),
)