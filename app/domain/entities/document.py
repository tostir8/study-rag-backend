from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    """
    Domain entity representing an indexed document.

    Every document belongs to a Study Room
    (tenant isolation).
    """

    id: str

    study_room_id: str

    filename: str

    file_path: str

    created_at: datetime

    is_active: bool = True
