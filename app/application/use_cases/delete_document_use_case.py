from pathlib import Path

from app.application.ports.document_repository_port import (
    DocumentRepositoryPort,
)
from app.application.ports.vector_store_port import (
    VectorStorePort,
)


class DeleteDocumentUseCase:
    """
    Deletes a document from the platform.

    It removes:

    - PostgreSQL metadata
    - ChromaDB embeddings
    - Uploaded PDF
    """

    def __init__(
        self,
        document_repository: DocumentRepositoryPort,
        vector_store: VectorStorePort,
    ) -> None:
        self._document_repository = document_repository
        self._vector_store = vector_store

    def execute(
        self,
        document_id: str,
    ) -> None:

        document = self._document_repository.get_by_id(
            document_id,
        )

        if document is None:
            raise ValueError(
                "Document not found."
            )

        self._vector_store.delete_document(
            document_id,
        )

        pdf = Path(
            document.file_path,
        )

        if pdf.exists():
            pdf.unlink()

        self._document_repository.delete(
            document_id,
        )
