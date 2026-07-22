from app.application.ports.document_repository_port import (
    DocumentRepositoryPort,
)
from app.domain.entities.document import Document


class ListDocumentsUseCase:
    """
    Returns all indexed documents.
    """

    def __init__(
        self,
        document_repository: DocumentRepositoryPort,
    ) -> None:
        self._document_repository = document_repository

    def execute(
        self,
    ) -> list[Document]:
        """
        Returns every indexed document.
        """

        return self._document_repository.list_all()
