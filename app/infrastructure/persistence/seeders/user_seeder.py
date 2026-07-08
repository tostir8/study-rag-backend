import uuid

from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.role_model import RoleModel
from app.infrastructure.security.password_service import hash_password


def seed_users(db):

    users = [
        {
            "name": "Admin User",
            "email": "admin@test.com",
            "password": "Admin123*",
            "role": "admin"
        },
        {
            "name": "Teacher User",
            "email": "teacher@test.com",
            "password": "Teacher123*",
            "role": "teacher"
        },
        {
            "name": "Student User",
            "email": "student@test.com",
            "password": "Student123*",
            "role": "student"
        }
    ]

    for user_data in users:

        existing_user = db.query(UserModel).filter(
            UserModel.email == user_data["email"]
        ).first()

        if existing_user:
            continue

        role = db.query(RoleModel).filter(
            RoleModel.name == user_data["role"]
        ).first()

        if not role:
            print(f"Rol {user_data['role']} no encontrado")
            continue

        user = UserModel(
            id=str(uuid.uuid4()),
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            role_id=role.id,
            is_verified=True,
            status="active"
        )

        db.add(user)

    db.commit()

    print("Usuarios de prueba creados correctamente")