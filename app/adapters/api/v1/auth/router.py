import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import secrets

from app.application.dto.auth.register_dto import RegisterDTO
from app.application.dto.auth.login_dto import LoginDTO
from app.application.dto.auth.refresh_dto import RefreshDTO
from app.application.dto.auth.logout_dto import LogoutDTO
from app.application.dto.auth.forgot_password_dto import ForgotPasswordDTO
from app.application.dto.auth.reset_password_dto import ResetPasswordDTO
from app.application.dto.auth.verify_email_dto import VerifyEmailDTO
from app.infrastructure.email.email_service import send_email
from app.infrastructure.persistence.session import get_db
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.security.password_service import hash_password, verify_password
from app.infrastructure.persistence.models.refresh_token_model import RefreshTokenModel
from app.infrastructure.security.jwt_service import create_access_token, create_refresh_token, decode_access_token
from app.infrastructure.security.permissions.auth_dependencies import get_current_user
from app.infrastructure.email.templates.verify_email_template import (
    get_verify_email_template
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Endpoint de registro de usuario
@router.post("/register")
async def register(data: RegisterDTO, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )
        
    verification_token = secrets.token_urlsafe(32)

    user = UserModel(
        id=str(uuid.uuid4()),
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role="student",
        email_verification_token=verification_token,
        is_verified="false"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    verify_link = (
        f"{os.getenv('FRONTEND_URL')}/verify-email?token={verification_token}"
    )

    subject, body = get_verify_email_template(
        user.name,
        verify_link
    )

    await send_email(
        to=user.email,
        subject=subject,
        body=body
    )

    return {
        "message": "Usuario registrado correctamente",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }
    
# Endpoint de login de usuario
@router.post("/login")
async def login(data: LoginDTO, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    refresh_token_record = RefreshTokenModel(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token=refresh_token,
        is_revoked=False
    )

    db.add(refresh_token_record)
    db.commit()

    return {
        "message": "Login exitoso",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }
    
@router.get("/me")
async def me(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }
#endpoint de refresh token@router.post("/refresh")
async def refresh(data: RefreshDTO, db: Session = Depends(get_db)):
    payload = decode_access_token(data.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Token de refresh inválido"
        )

    token_record = db.query(RefreshTokenModel).filter(
        RefreshTokenModel.token == data.refresh_token,
        RefreshTokenModel.is_revoked == False
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=401,
            detail="Refresh token revocado o inválido"
        )

    user_id = payload.get("sub")

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
    
#endpoint de logout
@router.post("/logout")
async def logout(
    data: LogoutDTO,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token_record = db.query(RefreshTokenModel).filter(
        RefreshTokenModel.token == data.refresh_token,
        RefreshTokenModel.user_id == current_user.id
    ).first()

    if not token_record:
        raise HTTPException(
            status_code=404,
            detail="Refresh token no encontrado"
        )

    token_record.is_revoked = True
    db.commit()

    return {
        "message": "Logout exitoso",
        "user": current_user.email
    }
#endpoint de forgot password
@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordDTO, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()

    if not user:
        return {
            "message": "Si el correo existe, se enviará un enlace de recuperación"
        }

    reset_token = secrets.token_urlsafe(32)
    user.reset_password_token = reset_token
    db.commit()

    reset_link = f"{os.getenv('FRONTEND_URL')}/reset-password?token={reset_token}"

    await send_email(
        to=user.email,
        subject="Restablecer contraseña - Study RAG",
        body=f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}"
    )

    return {
        "message": "Si el correo existe, se enviará un enlace de recuperación"
    }
#endpoint de reset password
@router.post("/reset-password")
async def reset_password(data: ResetPasswordDTO, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.reset_password_token == data.token).first()

    if not user:
        raise HTTPException(status_code=404, detail="Token de restablecimiento inválido")

    user.hashed_password = hash_password(data.new_password)
    user.reset_password_token = None
    db.commit()

    return {
        "message": "Contraseña restablecida exitosamente"
    }
#endpoint de verify email
@router.post("/verify-email")
async def verify_email(data: VerifyEmailDTO, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email_verification_token == data.token).first()

    if not user:
        raise HTTPException(status_code=404, detail="Token de verificación inválido")

    user.is_verified = "true"
    user.email_verification_token = None
    db.commit()

    return {
        "message": "Correo verificado exitosamente"
    }