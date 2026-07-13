from app.rag.document_loader import DocumentLoader
from app.rag.text_splitter import TextSplitter

loader = DocumentLoader(
    "../data/aws-three-tier-devsecops-platform"
)

documents = loader.load_documents()

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print()

print(f"Documents : {len(documents)}")

print(f"Chunks    : {len(chunks)}")

print()

print(chunks[0]["path"])

print()

print(chunks[0]["chunk"][:500])