import uuid

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_data.callback_data_notes import CallbackDataNotesDelete, CallbackDataNotesEdit


def get_note_inline(note_uuid: uuid.UUID) -> InlineKeyboardMarkup:
    """ Inline-keyboard under note to handle. """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить",
        callback_data=CallbackDataNotesEdit(id=note_uuid),
    )
    builder.button(
        text="Удалить",
        callback_data=CallbackDataNotesDelete(id=note_uuid),
    )
    return builder.as_markup()
