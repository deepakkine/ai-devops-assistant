import logging

from chromadb import PersistentClient

from app.core.config import CHROMADB_PATH
from app.rag.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, collection_name: str):
        self.client = PersistentClient(
            path=CHROMADB_PATH,
        )

        self.collection = self.client.get_collection(
            collection_name
        )

        self.embedding_service = EmbeddingService()

    def retrieve(
        self,
        question: str,
        k: int = 5,
    ):
        """
        Retrieve the most relevant chunks for a user's question
        using vector similarity search.
        """

        query_embedding = self.embedding_service.embed_query(
            question
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return [
            {
                "content": document,
                "metadata": metadata,
                "distance": distance,
            }
            for document, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def retrieve_project_context(
        self,
        k: int = 25,
    ):
        """
        Retrieve representative chunks from unique files
        to provide project-level context.
        """

        results = self.collection.get(
            include=[
                "documents",
                "metadatas",
            ],
        )

        logger.debug(
            "Collection=%s | Count=%d | Retrieved=%d",
            self.collection.name,
            self.collection.count(),
            len(results["documents"]),
        )

        docs: list[dict] = []
        seen: set[str] = set()

        # Keep only the first chunk from each file.
        for document, metadata in zip(
            results["documents"],
            results["metadatas"],
        ):
            path = metadata["path"]

            if path in seen:
                continue

            docs.append(
                {
                    "content": document,
                    "metadata": metadata,
                }
            )

            seen.add(path)

            if len(docs) >= k:
                break

        logger.debug(
            "Returning %d representative documents for project context.",
            len(docs),
        )

        return docs

    def retrieve_file_context(
        self,
        file_path: str,
    ):
        """
        Retrieve all indexed chunks for a specific file.
        """

        results = self.collection.get(
            where={
                "path": file_path,
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        docs = []

        for document, metadata in zip(
            results["documents"],
            results["metadatas"],
        ):
            docs.append(
                {
                    "content": document,
                    "metadata": metadata,
                }
            )

        return docs