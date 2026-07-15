import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def stream_gemini(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            logger.info("Trying Gemini model: %s", model)

            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
                max_retries=0,
                timeout=30,
            )

            for chunk in llm.stream(prompt):
                if chunk.content:
                    yield chunk.content

            return

        except Exception as e:
            logger.warning("%s failed: %s", model, e)
            last_error = e
            continue

    raise RuntimeError(
        "Unable to generate response from Gemini."
    ) from last_error


def ask_gemini(prompt: str):
    return "".join(stream_gemini(prompt))