import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .tag import NoteTag

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag


class Note(Base):
    __tablename__ = "note"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[str] = mapped_column()
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    author: Mapped["User"] = relationship(back_populates="notes")
    tags: Mapped[list["Tag"]] = relationship(
        back_populates="notes", secondary=NoteTag.__table__
    )

    def __repr__(self) -> str:
        return f"<Note(id={self.id!r}, title={self.title!r})>"

    def __str__(self) -> str:
        return f"<Note(id={self.id!r}, title={self.title!r})>"
