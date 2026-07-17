from app.application.ports.document_repository_port import (
    DocumentRepositoryPort,
)
from app.domain.entities.document import Document
from app.infrastructure.database.models.document_model import (
    DocumentModel,
)
from app.infrastructure.database.session import SessionLocal


class DocumentRepository(DocumentRepositoryPort):
    """
    SQLAlchemy implementation of the document repository.
    """

    def save(
        self,
        document: Document,
    ) -> None:

        session = SessionLocal()

        try:

            model = DocumentModel(
                id=document.id,
                study_room_id=document.study_room_id,
                filename=document.filename,
                file_path=document.file_path,
                created_at=document.created_at,
                is_active=document.is_active,
            )

            session.add(model)
            session.commit()

        finally:
            session.close()

    def get_by_id(
        self,
        document_id: str,
    ) -> Document | None:

        session = SessionLocal()

        try:

            model = session.get(
                DocumentModel,
                document_id,
            )

            if model is None:
                return None

            return Document(
                id=model.id,
                study_room_id=model.study_room_id,
                filename=model.filename,
                file_path=model.file_path,
                created_at=model.created_at,
                is_active=model.is_active,
            )

        finally:
            session.close()

    def list_all(
        self,
    ) -> list[Document]:

        session = SessionLocal()

        try:

            models = (
                session.query(DocumentModel)
                .filter(
                    DocumentModel.is_active.is_(True)
                )
                .order_by(
                    DocumentModel.created_at.desc()
                )
                .all()
            )

            return [
                Document(
                    id=model.id,
                    study_room_id=model.study_room_id,
                    filename=model.filename,
                    file_path=model.file_path,
                    created_at=model.created_at,
                    is_active=model.is_active,
                )
                for model in models
            ]

        finally:
            session.close()

    def delete(
        self,
        document_id: str,
    ) -> None:

        session = SessionLocal()

        try:

            model = session.get(
                DocumentModel,
                document_id,
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

        finally:
            session.close()
