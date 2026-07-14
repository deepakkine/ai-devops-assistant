from app.rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve("What is Docker?")

print(f"Retrieved {len(results)} results\n")

for i, result in enumerate(results, 1):
    print("=" * 80)
    print(f"Result {i}")
    print(f"Distance : {result['distance']:.4f}")
    print(result["metadata"])
    print()
    print(result["content"][:600])
    print()