from chromadb import PersistentClient

from app.rag.embedding_service import EmbeddingService


class Retriever:

    def __init__(self, collection_name: str):
        self.client = PersistentClient(
            path="./storage/chromadb"
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
        query_embedding = (
            self.embedding_service.embed_query(
                question
            )
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
        Return representative chunks for generating
        a project overview.
        """

        results = self.collection.get(
            include=[
                "documents",
                "metadatas",
            ],
        )

        docs = []

        seen = set()

        # README first
        for document, metadata in zip(
            results["documents"],
            results["metadatas"],
        ):
            path = metadata["path"]

            if "readme" in path.lower():
                docs.append(
                    {
                        "content": document,
                        "metadata": metadata,
                    }
                )

                seen.add(path)

        # One chunk per file
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

        return docs