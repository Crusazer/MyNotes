import logging
import uuid

from sqlalchemy import select, Select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.user import User
from src.core.schemas.user_schemas import SUserCreate

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self._session = db_session

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user bu given fields"""
        stmt: Select = select(User)
        stmt = stmt.where(User.email == email)
        result: Result = await self._session.execute(stmt)
        user: User = result.scalar()
        logger.info("Got user by email: %s.", email)

        return user

    async def get_user_by_id(self, user_uuid: uuid) -> User | None:
        """Get a user bu given fields"""
        stmt: Select = select(User)
        stmt = stmt.where(User.id == user_uuid)
        result: Result = await self._session.execute(stmt)
        user = result.scalars().first()
        return user

    async def create_user(self, new_user: SUserCreate) -> User:
        user = User(**new_user.model_dump())
        self._session.add(user)
        await self._session.commit()
        logger.info(f"Created new user: %s", new_user.email)
        return user
