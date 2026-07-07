from pydantic import BaseModel


class UpdateStatusDTO(BaseModel):
    status: str