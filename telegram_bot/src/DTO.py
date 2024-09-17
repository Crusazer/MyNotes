from pydantic import BaseModel


class TagDTO(BaseModel):
    name: str


class NoteDTO(BaseModel):
    title: str
    content: str
    tags: list[TagDTO]
