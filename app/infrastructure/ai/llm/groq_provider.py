from groq import Groq

from app.application.ports.llm_port import LLMPort
from app.config.settings import get_settings
from app.domain.exceptions.llm_exception import LLMException


class GroqProvider(LLMPort):
    """
    Groq implementation of the LLMPort.

    This adapter communicates with the Groq API while
    exposing the generic interface expected by the
    application layer.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        self._model = settings.LLM_MODEL

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> str:
        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )

            return response.choices[0].message.content or ""

        except Exception as exc:
            raise LLMException(
                f"Groq request failed: {exc}"
            ) from exc
