from abc import ABC
from abc import abstractmethod

from app.domain.entities.document import Document


class DocumentRepositoryPort(ABC):
    """
    Port for document persistence.
    """

    @abstractmethod
    def save(
        self,
        document: Document,
    ) -> None:
        pass

    @abstractmethod
    def get_by_id(
        self,
        document_id: str,
    ) -> Document | None:
        pass

    @abstractmethod
    def list_all(
        self,
    ) -> list[Document]:
        pass

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> None:
        """
        Deletes a document from persistence.
        """
        pass
