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
            logger.info(f"Trying Gemini model: {model}")

            llm = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=GEMINI_API_KEY,
                temperature=0.2,
                timeout=30,
                max_retries=0,
            )

            response = llm.invoke(prompt)

            logger.info(f"Model {model} succeeded")

            return response.content

        except Exception as e:
            logger.exception(f"Model {model} failed")
            print("=" * 80)
            print(f"MODEL FAILED: {model}")
            print(f"ERROR: {e}")
            print("=" * 80)
            last_error = e

    raise RuntimeError(
        "Unable to generate response from Gemini."
    ) from last_error


def stream_gemini(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            logger.info(f"Trying Gemini model: {model}")

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

            logger.info(f"Model {model} succeeded")

            return

        except Exception as e:
            logger.exception(f"Model {model} failed")
            print("=" * 80)
            print(f"MODEL FAILED: {model}")
            print(f"ERROR: {e}")
            print("=" * 80)
            last_error = e

    raise RuntimeError(
        "Unable to generate response from Gemini."
    ) from last_error