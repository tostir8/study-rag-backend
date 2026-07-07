from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.infrastructure.persistence.models.database import Base

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )