from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import GEMINI_API_KEY


class EmbeddingService:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GEMINI_API_KEY,
        )

    def embed_documents(self, texts):
        try:
            return self.embedding_model.embed_documents(texts)
        except Exception:
            print("=" * 80)
            print("EMBED DOCUMENTS FAILED")
            traceback.print_exc()
            print("=" * 80)
            raise

    def embed_query(self, text):
        return self.embedding_model.embed_query(text)