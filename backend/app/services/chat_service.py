from app.core.logger import logger
from app.core.gemini_client import ask_gemini
from app.prompts.prompt_builder import PromptBuilder
from app.rag.retriever import Retriever


class ChatService:

    def chat(
        self,
        question: str,
        repository: str,
        history=None,
    ):

        if history is None:
            history = []

        retriever = Retriever(repository)

        logger.info("Received question: %s", question)

        results = retriever.retrieve(question)

        relevant_results = [
            item
            for item in results
            if item["distance"] < 1.15
        ]

        relevant_docs = [
            item["content"]
            for item in relevant_results
        ]

        seen = set()
        sources = []

        for item in relevant_results:

            path = item["metadata"]["path"]

            if path not in seen:

                seen.add(path)

                sources.append(
                    {
                        "path": path,
                        "chunk_id": item["metadata"]["chunk_id"],
                    }
                )

        if not relevant_docs:

            logger.info("No relevant repository context found.")

            prompt = PromptBuilder.build(
                question=question,
                documents=[],
                history=history,
            )

            answer = ask_gemini(prompt)

            return {
                "answer": answer,
                "sources": [],
            }

        prompt = PromptBuilder.build(
            question=question,
            documents=relevant_docs,
            history=history,
        )

        answer = ask_gemini(prompt)

        logger.info("Repository-based response generated.")

        return {
            "answer": answer,
            "sources": sources,
        }