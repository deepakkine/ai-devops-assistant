from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GEMINI_API_KEY

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def ask_gemini(question: str) -> str:
    last_error = None

    for model in MODELS:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
            )

            response = llm.invoke(question)
            return response.content

        except Exception as e:
            print(f"[WARNING] {model} failed: {e}")
            last_error = e

    raise last_error