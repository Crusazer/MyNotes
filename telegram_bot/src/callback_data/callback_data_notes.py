import uuid

from aiogram.filters.callback_data import CallbackData


class CallbackDataNotesDelete(CallbackData, prefix="delete_note"):
    id: uuid.UUID


class CallbackDataNotesEdit(CallbackData, prefix="delete_edit"):
    id: uuid.UUID
