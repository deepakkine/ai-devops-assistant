import logging

from groq import Groq

from app.core.config import (
    DEFAULT_GROQ_MODEL,
    FALLBACK_GROQ_MODEL,
    GROQ_API_KEY,
)

logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

MODELS = (
    DEFAULT_GROQ_MODEL,
    FALLBACK_GROQ_MODEL,
)


def ask_groq(
    prompt: str,
    json_mode: bool = False,
):

    """
    Generate a response from Groq with automatic
    fallback between configured models.
    """

    last_error = None

    for model in MODELS:
        try:
            logger.info(
                "Trying Groq model: %s",
                model,
            )

            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": 0.2,
            }

            if json_mode:
                messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": (
                            "You are a JSON API. "
                            "Return ONLY valid JSON."
                        ),
                    },
                )

                kwargs["response_format"] = {
                    "type": "json_object"
                }

                kwargs["temperature"] = 0

            response = client.chat.completions.create(
                **kwargs
            )

            logger.info(
                "Groq model '%s' succeeded.",
                model,
            )

            return response.choices[0].message.content

        except Exception:
            logger.exception(
                "Groq model '%s' failed.",
                model,
            )
            last_error = e

    raise RuntimeError(
        "Unable to generate response from Groq."
    ) from last_error


def stream_groq(prompt: str):

    """
    Generate a streaming response from Groq with
    automatic fallback between configured models.
    """
    
    last_error = None

    for model in MODELS:
        try:
            logger.info(
                "Trying Groq model: %s",
                model,
            )

            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

            logger.info(
                "Groq model '%s' succeeded.",
                model,
            )
            return

        except Exception:
            logger.exception(
                "Groq model '%s' failed.",
                model,
            )
            last_error = e

    raise RuntimeError(
        "Unable to stream response from Groq."
    ) from last_error