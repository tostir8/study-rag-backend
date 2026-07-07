import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.application.dto.roles.create_role_dto import CreateRoleDTO
from app.application.dto.roles.update_role_dto import UpdateRoleDTO
from app.infrastructure.persistence.session import get_db
from app.infrastructure.persistence.models.role_model import RoleModel
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.security.permissions.auth_dependencies import get_current_user

router =  APIRouter(
    prefix="/roles",
    tags=["Roles"],
)

def require_admin(user: UserModel):
    if user.role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para realizar esta acción"
        )

def serialize_role(role: RoleModel):
    return {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "created_at": role.created_at
    }
    
#mostrar todos los roles
@router.get("/")
async def get_roles(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)
    roles = db.query(RoleModel).all()
    return [serialize_role(role) for role in roles]

#mostrar un rol por id
@router.get("/{role_id}")
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return serialize_role(role)

#crear un rol
@router.post("/")
async def create_role(
    data: CreateRoleDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    existing_role = db.query(RoleModel).filter(RoleModel.name == data.name).first()

    if existing_role:
        raise HTTPException(status_code=400, detail="El rol ya existe")

    role = RoleModel(
        id=str(uuid.uuid4()),
        name=data.name,
        description=data.description
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return {
        "message": "Rol creado correctamente",
        "role": serialize_role(role)
    }

#editar rol
@router.patch("/{role_id}")
async def update_role(
    role_id: str,
    data: UpdateRoleDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    if data.name is not None:
        existing_role = db.query(RoleModel).filter(
            RoleModel.name == data.name,
            RoleModel.id != role.id
        ).first()

        if existing_role:
            raise HTTPException(status_code=400, detail="El rol ya existe")

        role.name = data.name

    if data.description is not None:
        role.description = data.description

    db.commit()
    db.refresh(role)

    return {
        "message": "Rol actualizado correctamente",
        "role": serialize_role(role)
    }
    
#eliminar rol
@router.delete("/{role_id}")
async def delete_role(
    role_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    users_with_role = db.query(UserModel).filter(UserModel.role_id == role.id).count()

    if users_with_role > 0:
        raise HTTPException(
            status_code=400,
            detail="No puedes eliminar un rol asignado a usuarios"
        )

    db.delete(role)
    db.commit()

    return {
        "message": "Rol eliminado correctamente"
    }