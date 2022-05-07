import typing
from dataclasses import dataclass
import yaml

if typing.TYPE_CHECKING:
    from app.create_bot import Bot


@dataclass
class BotConfig:
    name: str
    username: str
    token: str
    api_id: int
    api_hash: str


@dataclass
class DatabaseConfig:
    login: str


@dataclass
class Config:
    bot: BotConfig = None
    db: DatabaseConfig = None


def setup_config(bot: "Bot", config_path: str) -> None:
    # Парсинг файла конфигурации
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    bot.config = Config(
        bot=BotConfig(
            name=raw_config["bot"]["name"],
            username=raw_config["bot"]["username"],
            token=raw_config["bot"]["token"],
            api_id=raw_config["bot"]["api_id"],
            api_hash=raw_config["bot"]["api_hash"],
            
        ),
        db=DatabaseConfig(
            login=raw_config["database"]["login"],
        ),
    )
