import logging
from typing import Optional
from aiogram import Bot as aioBot, Dispatcher
from config.config_reader import Config

class Bot():
    aiobot: Optional[aioBot] = None
    config: Optional[Config] = None
    dp: Optional[Dispatcher] = None
    logger: Optional[logging.Logger] = None
    #database: Optional[Database] = None

bot = Bot()