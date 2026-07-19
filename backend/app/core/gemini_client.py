import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
]


def ask_gemini(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            logger.info("Trying Gemini model: %s", model)

            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
                timeout=30,
                max_retries=0,
            )

            response = llm.invoke(prompt)

            return response.content

        except Exception as e:
            logger.exception("%s failed", model)
            last_error = e

    raise RuntimeError(
        "Unable to generate response from Gemini."
    ) from last_error


def stream_gemini(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            logger.info("Trying Gemini model: %s", model)

            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
                timeout=30,
                max_retries=0,
            )

            for chunk in llm.stream(prompt):
                if chunk.content:
                    yield chunk.content

            return

        except Exception as e:
            logger.exception("%s failed", model)
            last_error = e

    raise RuntimeError(
        "Unable to generate response from Gemini."
    ) from last_error