from app.core.logger import logger
from app.prompts.prompt_builder import PromptBuilder
from app.rag.retriever import Retriever
from app.core.gemini_client import ask_gemini


class ChatService:

    def __init__(self):
        self.retriever = Retriever()

    def chat(self, question: str):

        logger.info("Received question: %s", question)

        results = self.retriever.retrieve(question)

        documents = [
            item["content"]
            for item in results
        ]

        prompt = PromptBuilder.build(
            question,
            documents,
        )

        answer = ask_gemini(prompt)

        logger.info("Response generated successfully")

        return answer