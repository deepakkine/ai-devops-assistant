import shutil
import subprocess
from pathlib import Path

from chromadb import PersistentClient

from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore


class RepositoryService:

    DATA_DIR = Path("../data")

    def clone(self, github_url: str) -> str:

        repo_name = github_url.rstrip("/").split("/")[-1]

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

        loader = DocumentLoader(str(destination))
        documents = loader.load_documents()

        splitter = TextSplitter()
        chunks = splitter.split_documents(documents)

        store = VectorStore(repo_name)
        store.index_chunks(chunks)

        return repo_name

    def delete(self, repository_name: str):

        destination = self.DATA_DIR / repository_name

        if destination.exists():
            shutil.rmtree(destination)

        client = PersistentClient(
            path="./storage/chromadb"
        )

        try:
            client.delete_collection(repository_name)
        except Exception:
            pass

        return {
            "message": "Repository deleted successfully."
        }