from chromadb import PersistentClient

from app.rag.embedding_service import EmbeddingService


class VectorStore:

    def __init__(self, collection_name: str):

        self.client = PersistentClient(
            path="./storage/chromadb"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
        )

        self.embedding_service = EmbeddingService()

    def index_chunks(self, chunks):

        texts = [chunk["chunk"] for chunk in chunks]

        print(f"Generating embeddings for {len(texts)} chunks...")

        embeddings = self.embedding_service.embed_documents(texts)

        print(f"Generated {len(embeddings)} embeddings.")

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

        print("Writing embeddings to ChromaDB...")

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print("Successfully indexed repository.")

    def count(self):
        return self.collection.count()