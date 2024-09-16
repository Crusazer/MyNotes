import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .note import Note


class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    notes: Mapped[list["Note"]] = relationship(
        back_populates="tags", secondary="note_tag"
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id!r}, name={self.name!r})>"

    def __str__(self) -> str:
        return f"<Tag(id={self.id!r}, name={self.name!r})>"


class NoteTag(Base):
    __tablename__ = "note_tag"
    note_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("note.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
    )
