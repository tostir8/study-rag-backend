from sentence_transformers import SentenceTransformer

from app.application.ports.embedding_port import EmbeddingPort
from app.config.settings import get_settings


class SentenceTransformerEmbeddingProvider(EmbeddingPort):
    """
    Embedding provider based on Sentence Transformers.

    This adapter generates dense vector embeddings that
    will later be stored inside ChromaDB.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

    def embed(self, text: str) -> list[float]:
        """
        Generates an embedding vector from text.
        """
        embedding = self._model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()
