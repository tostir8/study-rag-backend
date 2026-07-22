from abc import ABC, abstractmethod


class LLMPort(ABC):
    """
    Contract that every Large Language Model provider
    must implement.

    The application layer depends only on this interface,
    never on a specific provider.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generates a response using a language model.

        Args:
            prompt: User prompt.
            system_prompt: Optional system instructions.
            temperature: Sampling temperature.
            max_tokens: Maximum number of tokens to generate.

        Returns:
            Generated text.
        """
        raise NotImplementedError
