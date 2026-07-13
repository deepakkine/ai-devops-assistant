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


def ask_gemini(question: str) -> str:
    last_error = None

    for model in MODELS:
        try:
            logger.info("Trying Gemini model: %s", model)

            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
            )

            response = llm.invoke(question)

            logger.info("Response generated using %s", model)

            return response.content

        except Exception as e:
            logger.warning("%s failed: %s", model, e)
            last_error = e

    logger.error("All Gemini models failed")

    raise RuntimeError("Unable to generate response from Gemini.") from last_error