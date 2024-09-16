import uuid

from pydantic import BaseModel


class STagGet(BaseModel):
    id: uuid.UUID


class STag(STagGet):
    name: str

    class Config:
        from_attributes = True
