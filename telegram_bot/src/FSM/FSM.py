from aiogram.fsm.state import StatesGroup, State


class RegisterNewUserState(StatesGroup):
    """ State to register new user """
    add_email = State()
    add_password = State()
