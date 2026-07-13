from chromadb import PersistentClient

from app.rag.embedding_service import EmbeddingService


class Retriever:

    def __init__(self):

        self.client = PersistentClient(
            path="./storage/chromadb"
        )

        self.collection = self.client.get_collection(
            "devops-repository"
        )

        self.embedding_service = EmbeddingService()

    def retrieve(self, question: str, k: int = 5):

        query_embedding = self.embedding_service.embed_query(question)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        return [
            {
                "content": document,
                "metadata": metadata,
            }
            for document, metadata in zip(
                results["documents"][0],
                results["metadatas"][0]
            )
        ]