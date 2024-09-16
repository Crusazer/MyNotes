import logging
import uuid

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.database.models.note import Note
from src.core.database.models.tag import Tag
from src.core.database.models.user import User
from src.core.schemas.note import SNote, SNoteCreate
from src.exceptions import TagNotFoundException

logger = logging.getLogger(__name__)


class NoteRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_all(self, user_id: uuid.UUID) -> list[SNote]:
        query = (
            select(User)
            .options(joinedload(User.notes).selectinload(Note.tags))
            .where(User.id == user_id)
        )
        result = await self._db_session.execute(query)
        user: User = result.scalars().first()
        notes: list[Note] = user.notes
        list_s_note = [
            SNote.model_validate(note, from_attributes=True) for note in notes
        ]
        return list_s_note

    async def create(self, user_id: uuid.UUID, s_note: SNoteCreate) -> SNote:
        tags_list: list[Tag] = []
        if s_note.tags:
            tags: Result = await self._db_session.execute(
                select(Tag).where(Tag.id.in_(s_note.tags))
            )
            tags_list: list[Tag] = tags.scalars().all()

        if len(s_note.tags) != len(tags_list):
            logger.info("Tags do not match")
            raise TagNotFoundException()

        note = Note(
            title=s_note.title, content=s_note.content, user_id=user_id, tags=tags_list
        )
        self._db_session.add(note)
        await self._db_session.commit()
        await self._db_session.refresh(note, attribute_names=["tags"])
        return SNote.model_validate(note, from_attributes=True)
