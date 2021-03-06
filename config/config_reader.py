from sys import intern
import typing
from dataclasses import dataclass
import yaml

if typing.TYPE_CHECKING:
    from app.create_bot import Bot


@dataclass
class BotConfig:
    token: str
    admin_id: int

@dataclass
class DatabaseConfig:
    table_id: str
    cred_file: str
    g_drive_media_folder: str

@dataclass
class ContactsConfig:
    admin_chanel_id: int
    new_user_chanel_id: int


@dataclass
class Config:
    bot: BotConfig = None
    db: DatabaseConfig = None
    contacts: ContactsConfig = None


def setup_config(bot: "Bot", config_path: str) -> None:
    # Парсинг файла конфигурации
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    bot.config = Config(
        bot=BotConfig(
            token=raw_config["bot"]["token"],
            admin_id=raw_config["bot"]["admin_id"],                       
        ),
        db=DatabaseConfig(
            table_id=raw_config["database"]["table_id"],
            cred_file=raw_config["database"]["cred_file"],
            g_drive_media_folder=raw_config["database"]["g_drive_media_folder"],
        ),
        contacts=ContactsConfig(
            admin_chanel_id=raw_config["contacts"]["admin_chanel_id"],
            new_user_chanel_id=raw_config["contacts"]["new_user_chanel_id"],
        ),
    )
