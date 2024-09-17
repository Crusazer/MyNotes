from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.FSM.FSM import RegisterNewUserState
from src.database import database as db
from src.database.database import User
from src.keyboards.reply import main_keyboard

router = Router()


@router.message(StateFilter(None), Command('start'))
async def start(message: Message, state: FSMContext):
    telegram_id: int = message.from_user.id
    user: User = await db.get_user_by_telegram_id(telegram_id)
    if user is None:
        await message.answer("Привет. Я бот для заметок. Для начала пройдите регистрацию. Введите свой email: ")
        await state.set_state(RegisterNewUserState.add_email)
    else:
        await message.answer(f"Вы уже зарегестрированы под email: {user.email}", reply_markup=main_keyboard())
