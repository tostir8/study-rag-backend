from fastapi import APIRouter
from pydantic import BaseModel

from app.application.use_cases.create_study_room_use_case import (
    CreateStudyRoomUseCase,
)
from app.application.use_cases.delete_study_room_use_case import (
    DeleteStudyRoomUseCase,
)
from app.application.use_cases.list_study_rooms_use_case import (
    ListStudyRoomsUseCase,
)
from app.infrastructure.database.repositories.study_room_repository import (
    StudyRoomRepository,
)

router = APIRouter(
    prefix="/study-rooms",
    tags=["Study Rooms"],
)


class CreateStudyRoomRequest(BaseModel):
    name: str
    description: str


@router.post("")
def create_room(
    request: CreateStudyRoomRequest,
):
    """
    Creates a Study Room.
    """

    room = CreateStudyRoomUseCase(
        repository=StudyRoomRepository(),
    ).execute(
        name=request.name,
        description=request.description,
    )

    return {
        "id": room.id,
        "name": room.name,
        "description": room.description,
        "created_at": room.created_at,
    }


@router.get("")
def list_rooms():
    """
    Returns every Study Room.
    """

    rooms = ListStudyRoomsUseCase(
        repository=StudyRoomRepository(),
    ).execute()

    return [
        {
            "id": room.id,
            "name": room.name,
            "description": room.description,
            "created_at": room.created_at,
            "is_active": room.is_active,
        }
        for room in rooms
    ]


@router.delete("/{room_id}")
def delete_room(
    room_id: str,
):
    """
    Deletes a Study Room.
    """

    DeleteStudyRoomUseCase(
        repository=StudyRoomRepository(),
    ).execute(
        room_id,
    )

    return {
        "message": "Study Room deleted successfully.",
    }
