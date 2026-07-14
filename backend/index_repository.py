from pathlib import Path

from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore


repo_path = "../data/aws-three-tier-devsecops-platform"
repo_name = Path(repo_path).name

print("\nLoading repository...")

loader = DocumentLoader(repo_path)

documents = loader.load_documents()

print(f"Loaded {len(documents)} documents")

print("\nSplitting documents...")

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print(f"Generated {len(chunks)} chunks")

print("\nGenerating embeddings and storing in ChromaDB...")

store = VectorStore(repo_name)

store.index_chunks(chunks)

print("\nIndexing completed successfully!")

print(f"Stored vectors: {store.count()}")