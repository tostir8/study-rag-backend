import uuid

from app.infrastructure.persistence.models.role_model import RoleModel


def seed_roles(db):
    roles = [
        {
            "name": "admin",
            "description": "Administrador del sistema"
        },
        {
            "name": "teacher",
            "description": "Profesor"
        },
        {
            "name": "student",
            "description": "Estudiante"
        }
    ]

    for role_data in roles:
        role_exists = db.query(RoleModel).filter(
            RoleModel.name == role_data["name"]
        ).first()

        if not role_exists:
            db.add(
                RoleModel(
                    id=str(uuid.uuid4()),
                    name=role_data["name"],
                    description=role_data["description"]
                )
            )

    db.commit()