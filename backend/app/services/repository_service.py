import logging
import shutil
import subprocess
from pathlib import Path

from chromadb import PersistentClient

from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)

class RepositoryService:

    DATA_DIR = Path("../data")

    def clone(self, github_url: str) -> str:
        """
        Clone a GitHub repository, process its documents,
        generate embeddings, and index them into ChromaDB.
        """

        repo_name = github_url.rstrip("/").split("/")[-1]

        logger.info("Cloning repository: %s", github_url)

        destination = self.DATA_DIR / repo_name

        if destination.exists():
            shutil.rmtree(destination)

        subprocess.run(
            [
                "git",
                "clone",
                github_url,
                str(destination),
            ],
            check=True,
        )

        logger.info("Repository cloned successfully to %s", destination)

        loader = DocumentLoader(str(destination))
        documents = loader.load_documents()

        splitter = TextSplitter()
        chunks = splitter.split_documents(documents)

        logger.info("Documents loaded: %d", len(documents))
        logger.info("Chunks created: %d", len(chunks))

        store = VectorStore(repo_name)

        try:
            logger.info("Starting embedding generation...")

            store.index_chunks(chunks)

            logger.info("Embedding generation completed.")

        except Exception:
            logger.exception("Error occurred while indexing repository '%s'", repo_name)
            raise

        return repo_name

    def delete(self, repository_name: str):
        """
        Delete a repository from local storage and remove
        its ChromaDB collection.
        """

        destination = self.DATA_DIR / repository_name

        if destination.exists():
            shutil.rmtree(destination)

        client = PersistentClient(
            path="./storage/chromadb"
        )

        try:
            client.delete_collection(repository_name)
        except Exception:
            logger.warning(
                "Collection '%s' does not exist or could not be deleted.",
                repository_name,
            )

        return {
            "message": "Repository deleted successfully."
        }