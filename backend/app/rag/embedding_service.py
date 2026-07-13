from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GEMINI_API_KEY


class EmbeddingService:

    def __init__(self):

        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GEMINI_API_KEY,
        )

    def embed_documents(self, chunks):

        texts = [
            chunk["chunk"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.embed_documents(texts)

        return embeddings