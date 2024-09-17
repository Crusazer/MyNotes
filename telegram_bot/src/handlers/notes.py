import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User

from src.FSM.FSM import CreateNoteState
from src.database import database as db
from src.keyboards.inline import get_note_inline
from src.manager import ApiManager

logger = logging.getLogger(__name__)
router = Router()


@router.message(StateFilter(None), F.text == "Показать все заметки")
async def all_notes(message: Message):
    user: User = await db.get_user_by_telegram_id(message.from_user.id)
    manager: ApiManager = ApiManager()
    notes: list[dict] = await manager.get_all_user_notes(user)

    if not notes:
        await message.answer(text="У вас нет заметок.")
    else:
        for note in notes:
            note_text = (f"<b>{note['title']}</b>\n"
                         f"{note['content']}\n"
                         f"{' '.join([tag["name"] for tag in note['tags']])}")
            await message.answer(
                text=note_text,
                reply_markup=get_note_inline(note["id"])
            )


@router.message(StateFilter(None), F.text == "Создать заметку")
async def create_notes(message: Message, state: FSMContext):
    await state.set_state(CreateNoteState.get_title)
    await message.answer(text="Напишите заголовок: ")


@router.message(StateFilter(CreateNoteState.get_title))
async def get_note_title(message: Message, state: FSMContext):
    """ Step 1. Get note title. """
    title = message.text
    if not title:
        await message.answer(text="Пожалуйста введите зоголовок: ")
    else:
        await state.update_data(title=title)
        await state.set_state(CreateNoteState.get_content)
        await message.answer(text="Введите текст заметки: ")

@router.message(StateFilter(CreateNoteState.get_content))
async def get_note_content(message: Message, state: FSMContext):
    """ Step 2. Get note content. """
    content = message.text
    if not content:
        await message.answer(text="Пожалуйста введите текст заметки:")
    else:
        await state.update_data(content=content)
        await state.set_state(CreateNoteState.get_tags)
        await message.answer("Введите теги через пробел. Например: #home #friends")

@router.message(StateFilter(CreateNoteState.get_tags))
async def get_note_tags(message: Message, state: FSMContext):
    """ Step 3. Get note tags. """
    tags: list[str] = message.text.strip().split()

    # Validate tags
    for tag in tags:
        if not tag.startswith("#"):
            await message.answer(text="Таг должен начинать с #. Введите теги повторно: ")
            return

    data: dict = await state.get_data()
    list_tags = [{"name": tag} for tag in tags]
    data.update({"tags": list_tags})
    user: User = await db.get_user_by_telegram_id(message.from_user.id)
    manager: ApiManager = ApiManager()
    text: str = await manager.create_note(user, data)
    await message.answer(text=text)
    await state.clear()

