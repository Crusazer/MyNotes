import aiosqlite
from pydantic import BaseModel

from src.config import settings


class User(BaseModel):
    telegram_id: int
    email: str
    access_token: str
    refresh_token: str


DATABASE_NAME = settings.DATABASE_NAME


async def init_db():
    """ Initialize the database """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                email TEXT UNIQUE NOT NULL,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL
            )
        ''')
        await db.commit()


async def add_user(user: User):
    """ Add new user to database """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            INSERT INTO users (email, telegram_id, access_token, refresh_token)
            VALUES (?, ?, ?, ?)
        ''', (user.email, user.telegram_id, user.access_token, user.refresh_token))
        await db.commit()


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    """ Get user by email"""
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute('''
            SELECT email, telegram_id, access_token, refresh_token
            FROM users
            WHERE telegram_id = ?
        ''', (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return User(email=row[0], telegram_id=row[1], access_token=row[2], refresh_token=row[3])
    return None


async def update_tokens(user: User):
    """ Update user tokens """
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute('''
            UPDATE users
            SET access_token = ?, refresh_token = ?
            WHERE telegram_id = ?
        ''', (user.access_token, user.refresh_token, user.telegram_id))
        await db.commit()
