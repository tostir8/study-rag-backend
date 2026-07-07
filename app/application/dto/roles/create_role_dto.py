from pydantic import BaseModel

class CreateRoleDTO(BaseModel):
    name: str
    description: str | None = None