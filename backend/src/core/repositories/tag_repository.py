import logging
from typing import List

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.tag import Tag
from src.core.schemas.tag import STag

logger = logging.getLogger(__name__)


class TagRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create(self, name: str) -> None:
        """Create a new tag"""
        tag = Tag(name=name)
        self._db_session.add(tag)
        await self._db_session.commit()
        logger.info(f"Tag %s created", name)

    async def get_all(self) -> List[STag]:
        """Get all tags"""
        stmt = select(Tag)
        result: Result = await self._db_session.execute(stmt)
        tags: list[Tag] = result.scalars().all()
        return [STag.model_validate(tag, from_attributes=True) for tag in tags]
