from pydantic import BaseModel
from typing import Optional


class UpdateSettingsDTO(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    study_reminders: Optional[bool] = None
    ai_model: Optional[str] = None