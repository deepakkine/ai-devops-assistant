from chromadb import PersistentClient
from app.rag.embedding_service import EmbeddingService


class VectorStore:

    def __init__(self):

        self.client = PersistentClient(
            path="./storage/chromadb"
        )

        self.collection = self.client.get_or_create_collection(
            name="devops-repository"
        )

        self.embedding_service = EmbeddingService()

    def index_chunks(self, chunks):

        texts = [chunk["chunk"] for chunk in chunks]

        embeddings = self.embedding_service.embed_documents(texts)

        ids = []

        metadatas = []

        for i, chunk in enumerate(chunks):

            ids.append(f"{chunk['path']}_{chunk['chunk_id']}")

            metadatas.append(
                {
                    "path": chunk["path"],
                    "chunk_id": chunk["chunk_id"],
                }
            )

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def count(self):

        return self.collection.count()