from pydantic import BaseModel


class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str