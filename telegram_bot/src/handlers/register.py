from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.FSM.FSM import RegisterNewUserState
from src.database import database as db
from src.database.database import User
from src.manager import ApiManager

router = Router()


@router.message(RegisterNewUserState.add_email)
async def get_email(message: Message, state: FSMContext):
    """ Step 1. Get email from user. """
    email = message.text

    # Simple validate email
    if '@' not in email:
        await message.answer(text="Введите корректный email.")
    else:
        # Save email and change state
        await state.update_data(email=email)
        await message.answer(text="Теперь введите пароль: ")
        await state.set_state(RegisterNewUserState.add_password)


@router.message(RegisterNewUserState.add_password)
async def get_password(message: Message, state: FSMContext):
    """ Step 2. Get password from user. And use api for register. """
    email = (await state.get_data())['email']
    password = message.text
    telegram_id = message.from_user.id

    manager: ApiManager = ApiManager()
    user: User | None = await manager.register_user(email, password, telegram_id)
    if user is None:
        # Error
        await state.set_state(RegisterNewUserState.add_password)
        await message.answer("Что-то пошло не так. Попробуйте ещё раз. Введите email: ")

    elif isinstance(user, User):
        # Success register
        await db.add_user(user)
        await message.answer(text="Регистрация успешно завершена!")
        await state.clear()

    else:
        # Return error message.
        await state.set_state(RegisterNewUserState.add_email)
        detail: list = user['detail']
        await message.answer(text=detail[0]['msg'].capitalize() + "\nВведите корректный email: ")
