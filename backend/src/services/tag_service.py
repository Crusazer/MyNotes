from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repositories.tag_repository import TagRepository
from src.core.schemas.tag import STag, STagGet


class TagService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self._tag_repository = TagRepository(db_session)

    async def create_tag(self, tag_name: str) -> None:
        """Create a new tag or"""
        await self._tag_repository.create(tag_name)

    async def get_all_tags(self) -> list[STag]:
        """Get all tags"""
        return await self._tag_repository.get_all()

    async def delete_tag(self, tag_uuid: STagGet) -> None:
        """Delete a tag if exists or raise HTTPException"""
        uuid: str = str(tag_uuid.id)
        await self._tag_repository.delete(uuid)
