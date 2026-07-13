from app.rag.document_loader import DocumentLoader

loader = DocumentLoader(
    "../data/aws-three-tier-devsecops-platform"
)

docs = loader.load_documents()

print(f"\nLoaded {len(docs)} documents\n")

for doc in docs[:10]:
    print(doc["path"])