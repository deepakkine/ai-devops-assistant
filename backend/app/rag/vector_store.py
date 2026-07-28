import logging

from chromadb import PersistentClient

from app.core.config import CHROMADB_PATH
from app.rag.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class VectorStore:

    def __init__(self, collection_name: str):

        self.client = PersistentClient(
            path=CHROMADB_PATH,
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
        )

        logger.info(
            "Using ChromaDB collection: %s",
            collection_name,
        )

        self.embedding_service = EmbeddingService()

    def index_chunks(self, chunks):
        """
        Generate embeddings for document chunks and store them
        in the ChromaDB collection.
        """

        texts = [chunk["chunk"] for chunk in chunks]

        logger.info(
            "Generating embeddings for %d chunks...",
            len(texts),
        )

        embeddings = self.embedding_service.embed_documents(texts)

        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )

        ids = []
        metadatas = []

        for chunk in chunks:

            ids.append(f"{chunk['path']}_{chunk['chunk_id']}")

            metadatas.append(
                {
                    "path": chunk["path"],
                    "chunk_id": chunk["chunk_id"],
                }
            )

        logger.info("Writing embeddings to ChromaDB...")

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info("Repository indexed successfully.")

    def count(self):
        """
        Return the total number of indexed chunks.
        """

        return self.collection.count()