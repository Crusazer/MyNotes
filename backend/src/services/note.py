import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.user import User
from src.core.repositories.note_repository import NoteRepository
from src.core.schemas.note import SNote, SNoteCreate

logger = logging.getLogger(__name__)


class NoteService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.note_repository = NoteRepository(db_session)

    async def get_all_notes(self, user: User) -> list[SNote]:
        notes: list[SNote] = await self.note_repository.get_all(user.id)
        return notes

    async def create_note(self, user: User, note: SNoteCreate) -> SNote:
        return await self.note_repository.create(user_id=user.id, s_note=note)
