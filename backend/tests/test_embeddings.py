from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter
from app.rag.embedding_service import EmbeddingService


loader = DocumentLoader(
    "../data/aws-three-tier-devsecops-platform"
)

documents = loader.load_documents()

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

embedding_service = EmbeddingService()

vectors = embedding_service.embed_documents(chunks[:5])

print()

print("Chunks :", len(chunks[:5]))

print("Vectors:", len(vectors))

print()

print("Embedding Dimension:", len(vectors[0]))