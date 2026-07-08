import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.application.dto.users.update_user_dto import UpdateUserDTO
from app.application.dto.users.update_role_dto import UpdateRoleDTO
from app.application.dto.users.change_password_dto import ChangePasswordDTO
from app.application.dto.users.update_settings_dto import UpdateSettingsDTO
from app.application.dto.users.update_status_dto import UpdateStatusDTO
from app.infrastructure.persistence.models.role_model import RoleModel
from app.infrastructure.security.password_service import hash_password, verify_password
from app.infrastructure.persistence.models.user_settings_model import UserSettingsModel
from app.infrastructure.persistence.models.refresh_token_model import RefreshTokenModel
from app.infrastructure.persistence.session import get_db
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.security.permissions.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def require_admin(current_user: UserModel):
    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo admin puede realizar esta acción"
        )
        
def serialize_user(user: UserModel):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.name if user.role else None,
        "role_id": user.role_id,
        "status": user.status,
        "avatar_url": user.avatar_url,
        "is_verified": user.is_verified,
        "last_login_at": user.last_login_at,
        "is_deleted": user.is_deleted,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
#mostrar todos los usuarios
@router.get("/")
async def get_users(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)
    users = db.query(UserModel).filter(UserModel.is_deleted == False).all()
    return [serialize_user(user) for user in users]

@router.get("/activity")
async def get_users_activity(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)

    total_users = db.query(UserModel).count()
    verified_users = db.query(UserModel).filter(UserModel.is_verified == True).count()

    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "unverified_users": total_users - verified_users
    }
    
#estatus del usurio
@router.get("/stats")
async def get_users_stats(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    total_users = db.query(UserModel).filter(
        UserModel.is_deleted == False
    ).count()

    verified_users = db.query(UserModel).filter(
        UserModel.is_verified == True,
        UserModel.is_deleted == False
    ).count()

    active_users = db.query(UserModel).filter(
        UserModel.status == "active",
        UserModel.is_deleted == False
    ).count()

    suspended_users = db.query(UserModel).filter(
        UserModel.status == "suspended",
        UserModel.is_deleted == False
    ).count()

    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "unverified_users": total_users - verified_users,
        "active_users": active_users,
        "suspended_users": suspended_users,
        "students": db.query(UserModel).join(RoleModel).filter(
        RoleModel.name == "student",
        UserModel.is_deleted == False
        ).count(),
        "teachers": db.query(UserModel).join(RoleModel).filter(
        RoleModel.name == "teacher",
        UserModel.is_deleted == False
        ).count(),
        "admins": db.query(UserModel).join(RoleModel).filter(
            RoleModel.name == "admin",
            UserModel.is_deleted == False
        ).count()
    }
    
#actualizar propio usuario
@router.patch("/me")
async def update_my_profile(
    data: UpdateUserDTO, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if data.name is not None:
        current_user.name = data.name

    if data.email is not None:
        existing_user = db.query(UserModel).filter(
            UserModel.email == data.email,
            UserModel.id != current_user.id
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está en uso"
            )

        current_user.email = data.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Perfil actualizado correctamente",
        "user": serialize_user(current_user)
    }

#cambiar avator del usuario
@router.put("/me/avatar")
async def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    folder = "uploads/avatars"
    os.makedirs(folder, exist_ok=True)

    extension = file.filename.split(".")[-1]
    filename = f"{current_user.id}-{uuid.uuid4()}.{extension}"
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.avatar_url = file_path
    db.commit()
    db.refresh(user)

    return {
        "message": "Avatar actualizado correctamente",
        "avatar_url": user.avatar_url
    }
    
#cambio de contraseña del usuario
@router.patch("/me/password")
async def change_my_password(
    data: ChangePasswordDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not verify_password(
        data.current_password,
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="La contraseña actual es incorrecta"
        )

    current_user.hashed_password = hash_password(
        data.new_password
    )

    db.query(RefreshTokenModel).filter(
        RefreshTokenModel.user_id == current_user.id
    ).update({
        "is_revoked": True
    })

    db.commit()

    return {
        "message": "Contraseña actualizada correctamente. Vuelve a iniciar sesión."
    }
    
#configuracion del usuario
@router.get("/me/settings")
async def get_my_settings(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    settings = db.query(UserSettingsModel).filter(
        UserSettingsModel.user_id == current_user.id
    ).first()

    if not settings:
        settings = UserSettingsModel(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    return {
        "user_id": current_user.id,
        "settings": {
            "theme": settings.theme,
            "language": settings.language,
            "notifications_enabled": settings.notifications_enabled,
            "email_notifications": settings.email_notifications,
            "study_reminders": settings.study_reminders,
            "ai_model": settings.ai_model
        }
    }
    
@router.patch("/me/settings")
async def update_my_settings(
    data: UpdateSettingsDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    settings = db.query(UserSettingsModel).filter(
        UserSettingsModel.user_id == current_user.id
    ).first()

    if not settings:
        settings = UserSettingsModel(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)

    if data.theme is not None:
        if data.theme not in ["light", "dark", "system"]:
            raise HTTPException(status_code=400, detail="Tema inválido")
        settings.theme = data.theme

    if data.language is not None:
        if data.language not in ["es", "en"]:
            raise HTTPException(status_code=400, detail="Idioma inválido")
        settings.language = data.language

    if data.notifications_enabled is not None:
        settings.notifications_enabled = data.notifications_enabled

    if data.email_notifications is not None:
        settings.email_notifications = data.email_notifications

    if data.study_reminders is not None:
        settings.study_reminders = data.study_reminders

    if data.ai_model is not None:
        settings.ai_model = data.ai_model

    db.commit()
    db.refresh(settings)

    return {
        "message": "Configuración actualizada correctamente",
        "settings": {
            "theme": settings.theme,
            "language": settings.language,
            "notifications_enabled": settings.notifications_enabled,
            "email_notifications": settings.email_notifications,
            "study_reminders": settings.study_reminders,
            "ai_model": settings.ai_model
        }
    }
    
#eliminar cuenta del usuario
@router.delete("/me")
async def delete_my_account(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    db.query(RefreshTokenModel).filter(
        RefreshTokenModel.user_id == current_user.id
    ).update({"is_revoked": True})

    current_user.is_deleted = True
    current_user.status = "inactive"

    db.commit()

    return {
        "message": "Cuenta eliminada correctamente"
    }
        
#mostrar un usuario por email
@router.get("/by-email/{email}")
async def get_user_by_email(email: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)
    user = db.query(UserModel).filter(UserModel.email == email, UserModel.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return serialize_user(user)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

#mostrar un usuario por id
@router.get("/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return serialize_user(user)

#actualizar un usuario
@router.patch("/{user_id}")
async def update_user( user_id: str, data: UpdateUserDTO, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)

    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if data.name is not None:
        user.name = data.name

    if data.email is not None:
        existing_user = db.query(UserModel).filter(
            UserModel.email == data.email,
            UserModel.id != user.id,
            UserModel.is_deleted == False
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El correo ya está en uso"
            )

        user.email = data.email

    db.commit()
    db.refresh(user)

    return {
        "message": "Usuario actualizado correctamente",
        "user": serialize_user(user)
    }

#actualizar el rol de un usuario
@router.patch("/{user_id}/role")
async def update_user_role(user_id: str, data: UpdateRoleDTO, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)

    role = db.query(RoleModel).filter(RoleModel.name == data.role).first()
    
    if not role:
        raise HTTPException(status_code=400, detail="Rol inválido")
        
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_deleted == False).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.role_id = role.id

    db.commit()
    db.refresh(user)

    return {
        "message": "Rol actualizado correctamente",
        "user": serialize_user(user)
    }

#eliminar un usuario
@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user.is_deleted = True
    user.status = "inactive"

    db.query(RefreshTokenModel).filter(
        RefreshTokenModel.user_id == user.id
    ).update({
        "is_revoked": True
    })

    db.commit()

    return {
        "message": "Usuario eliminado correctamente"
    }

#buscar documento por usuario
@router.get("/{user_id}/documents")
async def get_user_documents(user_id: str, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    require_admin(current_user)

    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "message": "endpoint en construcción todavia no esta conectado con la base de datos de documentos por que no existe todavia :C",
        "user_id": user.id,
        "documents": []
    }
    
#estatus del usuario
@router.patch("/{user_id}/status")
async def update_user_status(
    user_id: str,
    data: UpdateStatusDTO,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    require_admin(current_user)

    allowed_status = ["active", "inactive", "suspended", "banned"]

    if data.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Estado inválido"
        )

    user = db.query(UserModel).filter(
        UserModel.id == user_id,
        UserModel.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user.status = data.status

    if data.status != "active":
        db.query(RefreshTokenModel).filter(
            RefreshTokenModel.user_id == user.id
        ).update({"is_revoked": True})

    db.commit()
    db.refresh(user)

    return {
        "message": "Estado actualizado correctamente",
        "user": serialize_user(user)
    }