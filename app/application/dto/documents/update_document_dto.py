from pydantic import BaseModel
from typing import Optional


class UpdateDocumentDTO(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None