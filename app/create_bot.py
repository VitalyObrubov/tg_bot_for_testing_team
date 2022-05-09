import logging
from typing import Optional
from aiogram import Bot as aioBot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.globals import Bot, bot
from config.config_reader import setup_config
from app.handlers.start_end import register_handlers_common
from app.database.accessor import setup_db, load_users

def setup_logging(bot: Bot) -> None:
    # Настройка логирования в stdout

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot.logger = logging.getLogger(bot.config.bot.username)


def setup_aiogram(bot: Bot) -> None:
    bot.aiobot = aioBot(token = bot.config.bot.token)
    bot.dp = Dispatcher(bot.aiobot, storage=MemoryStorage())

async def set_commands(bot: aioBot):
    # Регистрация команд, отображаемых в интерфейсе Telegram
    
    commands = [
        BotCommand(command="/cancel", description="Отменить все и вернуться к началу")
    ]
    await bot.set_my_commands(commands)


async def setup_bot(config_path: str) -> Bot:
    setup_config(bot, config_path) 
    setup_logging(bot)
    setup_aiogram(bot)
    setup_db(bot)
    await load_users(bot)
    register_handlers_common(bot.dp)
    await set_commands(bot.aiobot)
    
    return bot