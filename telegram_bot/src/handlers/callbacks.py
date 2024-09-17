import logging
import uuid

from aiogram import Router
from aiogram.types import CallbackQuery

from src.callback_data.callback_data_notes import CallbackDataNotesEdit, CallbackDataNotesDelete
from src.database import database as db
from src.database.database import User
from src.manager import ApiManager

logger = logging.getLogger()
router: Router = Router()


@router.callback_query(CallbackDataNotesDelete.filter())
async def callback_note_delete(callback: CallbackQuery, callback_data: CallbackDataNotesDelete):
    """ Delete the note after press button """
    note_uuid: uuid.UUID = callback_data.id
    manager: ApiManager = ApiManager()
    user: User = await db.get_user_by_telegram_id(callback.from_user.id)
    text: str = await manager.delete_note(user, note_uuid)
    await callback.answer(text)


@router.callback_query(CallbackDataNotesEdit.filter())
async def callback_note_edit(callback: CallbackQuery, callback_data: CallbackDataNotesEdit):
    """ Edti the note after press button """
    note_uuid: uuid.UUID = callback_data.id
    manager: ApiManager = ApiManager()
    user: User = await db.get_user_by_telegram_id(callback.from_user.id)

    await callback.answer("Not implemented yet")
