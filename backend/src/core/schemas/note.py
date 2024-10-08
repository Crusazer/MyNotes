import uuid
from datetime import datetime

from pydantic import BaseModel

from .tag import STagCreate, STag


class SNoteCreate(BaseModel):
    title: str
    content: str
    tags: list["STagCreate"] | None


class SNote(SNoteCreate):
    id: uuid.UUID
    tags: list["STag"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SNoteEdit(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list["STagCreate"] | None = None
