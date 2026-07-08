from pydantic import BaseModel

class ResetPasswordDTO(BaseModel):
    token: str
    new_password: str