class PromptBuilder:

    @staticmethod
    def build(question: str, documents: list[str]) -> str:

        context = "\n\n".join(documents)

        return f"""
You are an expert DevOps Engineer.

Answer ONLY using the repository context below.

If the answer is not present in the repository, say:
"I couldn't find that information in the repository."

Repository Context:

{context}

Question:
{question}

Answer:
"""