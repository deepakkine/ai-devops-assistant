import logging

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)


class EmbeddingService:

    _embedding_model = None

    def __init__(self):
        if EmbeddingService._embedding_model is None:
            logger.info(
                "Loading embedding model: %s",
                EMBEDDING_MODEL,
            )

            EmbeddingService._embedding_model = (
                HuggingFaceEmbeddings(
                    model_name=EMBEDDING_MODEL,
                    model_kwargs={
                        "device": "cpu",
                    },
                    encode_kwargs={
                        "normalize_embeddings": True,
                    },
                )
            )
        else:
            logger.info(
                "Using cached embedding model."
            )

        self.embedding_model = (
            EmbeddingService._embedding_model
        )

    def embed_documents(self, texts):

        """
        Generate embeddings for a list of text chunks.
        """
        try:
            return self.embedding_model.embed_documents(texts)
        except Exception:
            logger.exception(
                "Failed to generate embeddings for %d documents.",
                len(texts),
            )
            raise

    def embed_query(self, text):

        """
        Generate an embedding for a single query.
        """
        try:
            return self.embedding_model.embed_query(text)
        except Exception:
            logger.exception(
                "Failed to generate embedding for query."
            )
            raise