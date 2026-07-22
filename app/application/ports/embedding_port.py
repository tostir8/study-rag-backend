from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    """
    Contract for embedding providers.

    The application layer should not know whether embeddings
    are generated using Sentence Transformers, OpenAI,
    Hugging Face, or any other provider.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generates an embedding vector from a text.

        Args:
            text: Input text.

        Returns:
            Numerical embedding vector.
        """
        raise NotImplementedError
