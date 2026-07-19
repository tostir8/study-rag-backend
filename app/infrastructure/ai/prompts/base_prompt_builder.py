from abc import ABC
from abc import abstractmethod
from typing import Any


class BasePromptBuilder(ABC):
    """
    Base class for every Prompt Builder in the platform.

    Responsibilities
    ----------------
    - Transform retrieved chunks into readable context.
    - Provide a common interface for every AI task.
    - Avoid duplicated logic between Chat, Exams,
      Flashcards and Summaries.
    """

    def build_context(
        self,
        contexts: list[dict[str, Any]],
    ) -> str:
        """
        Converts retrieved chunks into a single text block.
        """

        if not contexts:
            return "No relevant context was retrieved."

        return "\n\n".join(
            context["document"]
            for context in contexts
        )

    @abstractmethod
    def build(
        self,
        **kwargs,
    ) -> tuple[str, str]:
        """
        Builds the system prompt and user prompt.

        Returns
        -------
        tuple[str, str]

            (system_prompt, user_prompt)
        """
        raise NotImplementedError
