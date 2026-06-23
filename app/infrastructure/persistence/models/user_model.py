from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.infrastructure.persistence.models.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)
    reset_password_token = Column(String, nullable=True)
    email_verification_token = Column(String, nullable=True)
    is_verified = Column(String, default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())