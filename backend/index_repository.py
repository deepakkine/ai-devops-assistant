from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.vector_store import VectorStore


print("\nLoading repository...")

loader = DocumentLoader(
    "../data/aws-three-tier-devsecops-platform"
)

documents = loader.load_documents()

print(f"Loaded {len(documents)} documents")

print("\nSplitting documents...")

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print(f"Generated {len(chunks)} chunks")

print("\nGenerating embeddings and storing in ChromaDB...")

store = VectorStore()

store.index_chunks(chunks)

print()

print("Indexing completed successfully!")

print(f"Stored vectors: {store.count()}")