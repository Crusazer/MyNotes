import logging
import uuid

from sqlalchemy import select, Result, Select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.core.database.models.note import Note
from src.core.database.models.tag import Tag
from src.core.database.models.user import User
from src.core.schemas.note import SNote, SNoteCreate, SNoteEdit
from src.core.schemas.tag import STagCreate
from src.exceptions import NoteNotFoundException

logger = logging.getLogger(__name__)


class NoteRepository:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session

    async def get_by_uuid(self, user: User, note_uuid: uuid.UUID) -> SNote:
        """ Get note by uuid if exists and user is owned. """
        stmt: Select = (select(Note).
                        options(selectinload(Note.tags)).
                        where(and_(Note.uuid == note_uuid, Note.author == user))
                        )

        result: Result = await self._db_session.execute(stmt)
        note: Note = result.scalar().first()
        if note is None:
            raise NoteNotFoundException

        return SNote.model_validate(note, from_attributes=True)


    async def get_all(self, user_id: uuid.UUID) -> list[SNote]:
        """Get all notes of a user."""
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
        """Create new note if not exists and all tags exists."""
        tags_list: list["STag"] = [tag.name for tag in s_note.tags]
        tags_list: list[Tag] = await self._get_tag_list(tags_list)

        note = Note(
            title=s_note.title, content=s_note.content, user_id=user_id, tags=tags_list
        )
        self._db_session.add(note)
        await self._db_session.commit()
        await self._db_session.refresh(note, attribute_names=["tags"])
        return SNote.model_validate(note, from_attributes=True)

    async def delete(self, user: User, note_id: uuid.UUID) -> None:
        """Check whether a note exists, user is owned and delete it"""
        note: Note = await self._get_user_note(user, note_id)

        await self._db_session.delete(note)
        await self._db_session.commit()
        logger.info("Note %s deleted. Title: %s", note.id, note.title)

    async def edit(self, user: User, s_note_id: uuid.UUID, s_note: SNoteEdit) -> SNote:
        """Check whether a note exists, user is owned and edit it."""
        note: Note = await self._get_user_note(user, s_note_id)
        if s_note.title is not None:
            note.title = s_note.title

        if s_note.content is not None:
            note.content = s_note.content

        if s_note.tags is not None:
            tags_list: list["STagCreate"] = [tag.name for tag in s_note.tags]
            tags_list: list["STagCreate"] = await self._get_tag_list(tags_list)
            note.tags = tags_list

        await self._db_session.commit()
        await self._db_session.refresh(note, attribute_names=["tags", "updated_at"])
        logger.info("Note %s updated. Title: %s", note.id, note.title)
        return SNote.from_orm(note)

    async def _get_user_note(self, user: User, note_id: uuid.UUID) -> Note:
        """Get note if user it exists and user is owner."""
        stmt: Select = select(Note).where(and_(Note.author == user, Note.id == note_id))
        result: Result = await self._db_session.execute(stmt)
        note: Note = result.scalars().first()
        if note is None:
            logger.info("Note %s does not exist", note_id)
            raise NoteNotFoundException()
        return note

    async def _get_tag_list(self, tag_names: list["STagCreate"]) -> list[Tag]:
        """Get existing tags by names and create new ones if they don't exist."""

        # Step 1: Fetch existing tags
        existing_tags_stmt = select(Tag).where(Tag.name.in_(tag_names))
        result = await self._db_session.execute(existing_tags_stmt)
        existing_tags = result.scalars().all()

        # Extract names of existing tags
        existing_tag_names = {tag.name for tag in existing_tags}

        # Determine which tags are missing
        missing_tag_names = set(tag_names) - existing_tag_names

        # Step 2: Create missing tags
        if missing_tag_names:
            # Bulk insert for efficiency
            for name in missing_tag_names:
                new_tag = Tag(name=name)
                self._db_session.add(new_tag)

            # Commit changes so the new tags are persisted in the database
            await self._db_session.commit()

            # Fetch all tags again, including newly created ones
            result = await self._db_session.execute(select(Tag).where(Tag.name.in_(tag_names)))
            all_tags = result.scalars().all()
        else:
            all_tags = existing_tags

        return all_tags
