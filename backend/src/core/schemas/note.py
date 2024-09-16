import uuid
from datetime import datetime

from pydantic import BaseModel

from .tag import STag


class SNoteCreate(BaseModel):
    title: str
    content: str
    tags: list[uuid.UUID] | None


class SNote(SNoteCreate):
    id: uuid.UUID
    tags: list["STag"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
