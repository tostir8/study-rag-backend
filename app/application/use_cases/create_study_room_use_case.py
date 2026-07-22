from datetime import datetime
from uuid import uuid4

from app.application.ports.study_room_repository_port import (
    StudyRoomRepositoryPort,
)
from app.domain.entities.study_room import StudyRoom


class CreateStudyRoomUseCase:
    """
    Creates a new Study Room.
    """

    def __init__(
        self,
        repository: StudyRoomRepositoryPort,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        name: str,
        description: str,
    ) -> StudyRoom:
        """
        Creates and persists a Study Room.
        """

        room = StudyRoom(
            id=str(uuid4()),
            name=name,
            description=description,
            created_at=datetime.utcnow(),
        )

        self._repository.save(room)

        return room
