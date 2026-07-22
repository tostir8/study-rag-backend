from abc import ABC
from abc import abstractmethod

from app.domain.entities.study_room import StudyRoom


class StudyRoomRepositoryPort(ABC):
    """
    Port for Study Room persistence.
    """

    @abstractmethod
    def save(
        self,
        room: StudyRoom,
    ) -> None:
        pass

    @abstractmethod
    def get_by_id(
        self,
        room_id: str,
    ) -> StudyRoom | None:
        pass

    @abstractmethod
    def list_all(
        self,
    ) -> list[StudyRoom]:
        pass

    @abstractmethod
    def delete(
        self,
        room_id: str,
    ) -> None:
        pass
