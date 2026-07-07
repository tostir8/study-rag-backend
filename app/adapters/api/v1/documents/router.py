import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.application.dto.documents.update_document_dto import UpdateDocumentDTO
from app.infrastructure.persistence.session import get_db
from app.infrastructure.persistence.models.document_model import DocumentModel
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.security.permissions.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

def serialize_document(document: DocumentModel):
    return {
        "id": document.id,
        "user_id": document.user_id,
        "title": document.title,
        "file_name": document.file_name,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "file_path": document.file_path,
        "status": document.status,
        "is_processed": document.is_processed,
        "created_at": document.created_at,
        "updated_at": document.updated_at
    }


#subir documentos
@router.post("/upload")
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    allowed_types = ["pdf", "docx", "txt"]

    extension = file.filename.split(".")[-1].lower()

    if extension not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Tipo de archivo no permitido"
        )

    folder = "uploads/documents"
    os.makedirs(folder, exist_ok=True)

    file_id = str(uuid.uuid4())
    file_name = f"{file_id}-{file.filename}"
    file_path = os.path.join(folder, file_name)

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    document = DocumentModel(
        id=file_id,
        user_id=current_user.id,
        title=title,
        file_name=file.filename,
        file_type=extension,
        file_size=str(len(content)),
        file_path=file_path,
        status="uploaded",
        is_processed=False
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "Documento subido correctamente",
        "document": serialize_document(document)
    }
    
@router.get("/")
async def get_my_documents(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    documents = db.query(DocumentModel).filter(
        DocumentModel.user_id == current_user.id
    ).all()

    return [serialize_document(document) for document in documents]


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if document.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")

    return serialize_document(document)


@router.patch("/{document_id}")
async def update_document(
    document_id: str,
    data: UpdateDocumentDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if document.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")

    if data.title is not None:
        document.title = data.title

    if data.status is not None:
        document.status = data.status

    db.commit()
    db.refresh(document)

    return {
        "message": "Documento actualizado correctamente",
        "document": serialize_document(document)
    }

#eliminar documento
@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    document = db.query(DocumentModel).filter(
        DocumentModel.id == document_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if document.user_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return {
        "message": "Documento eliminado correctamente"
    }