from app.application.ports.study_room_repository_port import (
    StudyRoomRepositoryPort,
)
from app.domain.entities.study_room import StudyRoom
from app.infrastructure.database.models.study_room_model import (
    StudyRoomModel,
)
from app.infrastructure.database.session import SessionLocal


class StudyRoomRepository(StudyRoomRepositoryPort):
    """
    SQLAlchemy implementation of the Study Room repository.
    """

    def save(
        self,
        room: StudyRoom,
    ) -> None:

        session = SessionLocal()

        try:

            model = StudyRoomModel(
                id=room.id,
                name=room.name,
                description=room.description,
                created_at=room.created_at,
                is_active=room.is_active,
            )

            session.add(model)
            session.commit()

        finally:
            session.close()

    def get_by_id(
        self,
        room_id: str,
    ) -> StudyRoom | None:

        session = SessionLocal()

        try:

            model = session.get(
                StudyRoomModel,
                room_id,
            )

            if model is None:
                return None

            return StudyRoom(
                id=model.id,
                name=model.name,
                description=model.description,
                created_at=model.created_at,
                is_active=model.is_active,
            )

        finally:
            session.close()

    def list_all(
        self,
    ) -> list[StudyRoom]:

        session = SessionLocal()

        try:

            models = (
                session.query(StudyRoomModel)
                .filter(
                    StudyRoomModel.is_active.is_(True)
                )
                .order_by(
                    StudyRoomModel.created_at.desc()
                )
                .all()
            )

            return [
                StudyRoom(
                    id=model.id,
                    name=model.name,
                    description=model.description,
                    created_at=model.created_at,
                    is_active=model.is_active,
                )
                for model in models
            ]

        finally:
            session.close()

    def delete(
        self,
        room_id: str,
    ) -> None:

        session = SessionLocal()

        try:

            model = session.get(
                StudyRoomModel,
                room_id,
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

        finally:
            session.close()
