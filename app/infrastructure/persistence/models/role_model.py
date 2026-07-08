from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.infrastructure.persistence.models.database import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )