from abc import ABC
from abc import abstractmethod
from typing import Any


class VectorStorePort(ABC):
    """
    Contract for vector databases.
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
        Stores embeddings.
        """
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Searches similar vectors.
        """
        pass

    @abstractmethod
    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Removes every chunk belonging to a document.
        """
        pass
