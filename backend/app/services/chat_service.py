from app.prompts.prompt_builder import PromptBuilder
from app.rag.retriever import Retriever
from app.core.gemini_client import ask_gemini


class ChatService:

    def __init__(self):
        self.retriever = Retriever()

    def chat(self, question: str):

        results = self.retriever.retrieve(question)

        documents = [
            item["content"]
            for item in results
        ]
        prompt = PromptBuilder.build(
            question=question,
            documents=documents
        )

        return ask_gemini(prompt)