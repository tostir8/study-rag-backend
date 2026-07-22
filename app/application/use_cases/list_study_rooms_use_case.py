from app.application.ports.study_room_repository_port import (
    StudyRoomRepositoryPort,
)
from app.domain.entities.study_room import StudyRoom


class ListStudyRoomsUseCase:
    """
    Returns every active Study Room.
    """

    def __init__(
        self,
        repository: StudyRoomRepositoryPort,
    ) -> None:
        self._repository = repository

    def execute(
        self,
    ) -> list[StudyRoom]:
        """
        Returns all Study Rooms.
        """

        return self._repository.list_all()
