import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base
from .note import Note


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_staff: Mapped[bool] = mapped_column(nullable=False, default=False)
    notes: Mapped[list["Note"]] = relationship()

    def __str__(self):
        return str(self.email)

    def __repr__(self):
        return str(self.email)
