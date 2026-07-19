class EmbeddingService:
    def __init__(self):
        print("Using FAKE EmbeddingService")

    def embed_documents(self, texts):
        print(f"Generating fake embeddings for {len(texts)} chunks...")

        # all-MiniLM-L6-v2 produces 384-dimensional embeddings
        return [[0.0] * 384 for _ in texts]

    def embed_query(self, text):
        return [0.0] * 384