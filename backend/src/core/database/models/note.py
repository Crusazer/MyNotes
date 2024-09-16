import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag


class Note(Base):
    __tablename__ = "note"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[str] = mapped_column()
    author: Mapped["User"] = relationship()
    tags: Mapped[list["Tag"]] = relationship(back_populates="notes", secondary="notes_tags")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)

    def __repr__(self) -> str:
        return f"<Note(id={self.id!r}, title={self.title!r})>"

    def __str__(self) -> str:
        return f"<Note(id={self.id!r}, title={self.title!r})>"


class NoteTag(Base):
    __tablename__ = "note_tag"
    note_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("note.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tag.id"), onupdate="CASCADE", primary_key=True)