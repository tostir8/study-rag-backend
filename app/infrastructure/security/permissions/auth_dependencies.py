from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.persistence.session import get_db
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.security.jwt_service import decode_access_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Token incorrecto")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Token sin usuario")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if user.is_deleted:
        raise HTTPException(status_code=403, detail="La cuenta fue eliminada")

    if user.status != "active":
        raise HTTPException(status_code=403, detail="La cuenta está deshabilitada")

    return user