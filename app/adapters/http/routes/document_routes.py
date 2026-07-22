from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.application.use_cases.index_document_use_case import (
    IndexDocumentUseCase,
)
from app.application.use_cases.list_documents_use_case import (
    ListDocumentsUseCase,
)
from app.infrastructure.ai.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from app.infrastructure.ai.rag.chunker import Chunker
from app.infrastructure.database.repositories.document_repository import (
    DocumentRepository,
)
from app.infrastructure.database.repositories.study_room_repository import (
    StudyRoomRepository,
)
from app.infrastructure.storage.pdf_loader import PDFLoader
from app.infrastructure.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIRECTORY = Path("storage/uploads")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/study-room/{study_room_id}/upload")
async def upload_document(
    study_room_id: str,
    file: UploadFile = File(...),
):
    """
    Uploads a PDF into a Study Room.
    """

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    room = StudyRoomRepository().get_by_id(
        study_room_id,
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Study Room not found.",
        )

    document_id = str(uuid4())

    file_path = (
        UPLOAD_DIRECTORY /
        f"{document_id}.pdf"
    )

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    use_case = IndexDocumentUseCase(
        loader=PDFLoader(),
        chunker=Chunker(),
        embedding_provider=SentenceTransformerEmbeddingProvider(),
        vector_store=ChromaVectorStore(),
        document_repository=DocumentRepository(),
    )

    use_case.execute(
        document_id=document_id,
        study_room_id=study_room_id,
        filename=file.filename,
        pdf_path=str(file_path),
    )

    return {
        "message": "Document indexed successfully.",
        "study_room_id": study_room_id,
        "document_id": document_id,
    }


@router.get("")
def list_documents():
    """
    Returns every indexed document.
    """

    use_case = ListDocumentsUseCase(
        document_repository=DocumentRepository(),
    )

    documents = use_case.execute()

    return [
        {
            "id": document.id,
            "study_room_id": document.study_room_id,
            "filename": document.filename,
            "created_at": document.created_at,
            "is_active": document.is_active,
        }
        for document in documents
    ]
