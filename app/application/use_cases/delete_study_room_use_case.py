from app.application.ports.study_room_repository_port import (
    StudyRoomRepositoryPort,
)


class DeleteStudyRoomUseCase:
    """
    Deletes a Study Room.
    """

    def __init__(
        self,
        repository: StudyRoomRepositoryPort,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        room_id: str,
    ) -> None:
        """
        Deletes a Study Room.
        """

        self._repository.delete(room_id)
