from pydantic import BaseModel


class UpdateRoleDTO(BaseModel):
    role: str