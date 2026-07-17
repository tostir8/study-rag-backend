from datetime import datetime

from app.application.ports.document_repository_port import (
    DocumentRepositoryPort,
)
from app.application.ports.embedding_port import EmbeddingPort
from app.application.ports.vector_store_port import VectorStorePort
from app.domain.entities.document import Document
from app.infrastructure.ai.rag.chunker import Chunker
from app.infrastructure.storage.pdf_loader import PDFLoader


class IndexDocumentUseCase:
    """
    Indexes a PDF document into the platform.

    Pipeline:

    Study Room
        ↓
    Persist document metadata
        ↓
    Extract text
        ↓
    Chunk text
        ↓
    Generate embeddings
        ↓
    Store embeddings into ChromaDB
    """

    def __init__(
        self,
        loader: PDFLoader,
        chunker: Chunker,
        embedding_provider: EmbeddingPort,
        vector_store: VectorStorePort,
        document_repository: DocumentRepositoryPort,
    ) -> None:
        self._loader = loader
        self._chunker = chunker
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._document_repository = document_repository

    def execute(
        self,
        document_id: str,
        study_room_id: str,
        filename: str,
        pdf_path: str,
    ) -> None:
        """
        Indexes an entire PDF document.
        """

        document = Document(
            id=document_id,
            study_room_id=study_room_id,
            filename=filename,
            file_path=pdf_path,
            created_at=datetime.utcnow(),
        )

        self._document_repository.save(
            document,
        )

        text = self._loader.load(
            pdf_path,
        )

        chunks = self._chunker.split(
            text,
        )

        embeddings = [
            self._embedding_provider.embed(chunk)
            for chunk in chunks
        ]

        metadata = [
            {
                "document_id": document_id,
                "study_room_id": study_room_id,
                "chunk": index,
            }
            for index in range(len(chunks))
        ]

        self._vector_store.add(
            document_id=document_id,
            embeddings=embeddings,
            documents=chunks,
            metadata=metadata,
        )
