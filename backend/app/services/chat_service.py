from app.core.gemini_client import ask_gemini


class ChatService:

    @staticmethod
    def chat(question: str) -> str:
        return ask_gemini(question)