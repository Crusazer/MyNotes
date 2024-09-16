import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base

if TYPE_CHECKING:
    from .note import Note


class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)
    notes: Mapped[list[Note]] = relationship(back_populates="tags", secondary="note_tag")

    def __repr__(self) -> str:
        return f"<Tag(id={self.id!r}, title={self.title!r})>"

    def __str__(self) -> str:
        return f"<Tag(id={self.id!r}, title={self.title!r})>"
