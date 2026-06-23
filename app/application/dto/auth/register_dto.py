from pydantic import BaseModel, EmailStr

class RegisterDTO(BaseModel):
    name: str
    email: EmailStr
    password: str