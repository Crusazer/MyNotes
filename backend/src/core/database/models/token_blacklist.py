import datetime

from sqlalchemy import Column, Integer, UUID, DateTime, func
from sqlalchemy.orm import Mapped

from .base import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"
    id: Mapped[Integer] = Column(Integer, primary_key=True, autoincrement=True)
    jti: Mapped[UUID] = Column(
        UUID(as_uuid=True), nullable=False, unique=True, index=True
    )
    blacklisted_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"TokenBlacklist jti={self.jti}"
