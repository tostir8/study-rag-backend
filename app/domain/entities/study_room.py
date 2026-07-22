from dataclasses import dataclass
from datetime import datetime


@dataclass
class StudyRoom:
    """
    Domain entity representing a study room.

    A Study Room acts as a tenant where users
    collaborate with shared documents.
    """

    id: str

    name: str

    description: str

    created_at: datetime

    is_active: bool = True
