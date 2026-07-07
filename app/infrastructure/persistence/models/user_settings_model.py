from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.infrastructure.persistence.models.database import Base

class UserSettingsModel(Base):
    __tablename__ = "user_settings"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    theme = Column(String, default="light", nullable=False)
    language = Column(String, default="es", nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    email_notifications = Column(Boolean, default=True, nullable=False)
    study_reminders = Column(Boolean, default=True, nullable=False)
    ai_model = Column(String, default="gpt-4o-mini",nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )