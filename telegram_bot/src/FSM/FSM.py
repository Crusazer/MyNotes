from aiogram.fsm.state import StatesGroup, State


class RegisterNewUserState(StatesGroup):
    """ State to register new user """
    add_email = State()
    add_password = State()


class CreateNoteState(StatesGroup):
    """ State to create new note """
    get_title = State()
    get_content = State()
    get_tags = State()
