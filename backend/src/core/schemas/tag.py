import uuid

from pydantic import BaseModel


class STagGet(BaseModel):
    id: uuid.UUID


class STagCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class STag(STagCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True
