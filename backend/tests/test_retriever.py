from app.rag.retriever import Retriever

retriever = Retriever()

question = "How is the VPC created?"

results = retriever.retrieve(question)

print()

print("Question:")
print(question)

print()

for i, doc in enumerate(results["documents"][0], start=1):

    print("=" * 80)

    print(f"Result {i}")

    print()

    print(doc[:600])