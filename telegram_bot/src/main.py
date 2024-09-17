import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from src.config import settings
from src.database.database import init_db
from src.handlers.callbacks import router as callbacks_router
from src.handlers.commands import router as commands_router
from src.handlers.notes import router as notes_router
from src.handlers.register import router as register_router
from src.logger.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot...")
    await init_db()
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    """ Register router """
    dp.include_router(notes_router)
    dp.include_router(commands_router)
    dp.include_router(register_router)
    dp.include_router(callbacks_router)

    try:
        logger.info("Bot started.")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await asyncio.wait_for(bot.session.close(), timeout=10)


if __name__ == '__main__':
    asyncio.run(main())
