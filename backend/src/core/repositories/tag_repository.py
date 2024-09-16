import logging
from typing import List

from sqlalchemy import Result, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.tag import Tag
from src.core.schemas.tag import STag
from src.exceptions import TagNotFoundException, TagAlreadyExistsException

logger = logging.getLogger(__name__)


class TagRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def create(self, name: str) -> None:
        """Create a new tag or raise HTTP exception if tag with this name already exists."""
        # Check existing
        stmt: Select = select(Tag).where(Tag.name == name)
        result: Result = await self._db_session.execute(stmt)
        if result.scalar():
            logger.info("Tag with name %s already exists", name)
            raise TagAlreadyExistsException()

        # Create new tag
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

    async def delete(self, uuid: str) -> None:
        """Delete existing tag"""
        stmt = select(Tag).where(Tag.id == uuid)
        result: Result = await self._db_session.execute(stmt)
        tag: Tag = result.scalar_one_or_none()
        if tag is None:
            logger.info(f"Tag %s not found", uuid)
            raise TagNotFoundException()
        await self._db_session.delete(tag)
        await self._db_session.commit()
        logger.info(f"Tag %s deleted", uuid)
