import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)

logger = logging.getLogger(__name__)


class TextSplitter:

    def __init__(
        self,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split_documents(self, documents):
        """
        Split repository documents into smaller chunks for embedding.
        """

        chunks = []

        for document in documents:

            splits = self.splitter.split_text(document["content"])

            logger.debug(
                "Split '%s' into %d chunks.",
                document["path"],
                len(splits),
            )

            for index, chunk in enumerate(splits):

                chunks.append(
                    {
                        "path": document["path"],
                        "chunk": chunk,
                        "chunk_id": index,
                    }
                )

        logger.info(
            "Created %d chunks from %d documents.",
            len(chunks),
            len(documents),
        )

        return chunks