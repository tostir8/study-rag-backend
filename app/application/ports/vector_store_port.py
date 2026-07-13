from abc import ABC, abstractmethod
from typing import Any


class VectorStorePort(ABC):
    """
    Contract for vector databases.

    The application layer should not know whether vectors
    are stored in ChromaDB, FAISS, Pinecone, Qdrant,
    pgvector, or any other implementation.
    """

    @abstractmethod
    def add(
        self,
        document_id: str,
        embeddings: list[list[float]],
        documents: list[str],
        metadata: list[dict[str, Any]],
    ) -> None:
        """
        Stores embeddings and their associated metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieves the most relevant chunks.
        """
        raise NotImplementedError
