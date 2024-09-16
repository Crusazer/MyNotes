from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.tag_repository import TagRepository
from src.core.schemas.tag import STag


class TagService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._tag_repository = TagRepository(db_session)

    async def create_tag(self, tag_name: str) -> None:
        await self._tag_repository.create(tag_name)

    async def get_all_tags(self) -> list[STag]:
        return await self._tag_repository.get_all()
