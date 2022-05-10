import logging
from aiogram import Bot as aioBot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.globals import Bot, bot
from config.config_reader import setup_config
from app.handlers.start_end import register_handlers_common
from app.database.accessor import GoogleDatabase

def setup_logging(bot: Bot) -> None:
    # Настройка логирования в stdout

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot.logger = logging.getLogger(bot.config.bot.username)


def setup_aiogram(bot: Bot) -> None:
    bot.aiobot = aioBot(token = bot.config.bot.token, parse_mode="HTML")
    bot.dp = Dispatcher(bot.aiobot, storage=MemoryStorage())

def setup_db(bot: Bot) -> None:
    bot.database = GoogleDatabase(bot)

async def setup_bot(config_path: str) -> Bot:
    setup_config(bot, config_path) 
    setup_logging(bot)
    setup_aiogram(bot)
    setup_db(bot)
    await bot.database.load_users(bot)
    register_handlers_common(bot.dp)
    
    return bot