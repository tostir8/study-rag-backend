from pydantic import BaseModel, EmailStr
from typing import Optional

class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None