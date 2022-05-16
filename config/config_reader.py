from sys import intern
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
    admin_id: int
    api_id: int
    api_hash: str

@dataclass
class DatabaseConfig:
    table_id: str
    cred_file: str
    g_drive_media_folder: str

@dataclass
class ContactsConfig:
    common_chanel: str
    admin_chanel: str
    admin_chanel_id: int

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
            name=raw_config["bot"]["name"],
            username=raw_config["bot"]["username"],
            token=raw_config["bot"]["token"],
            admin_id=raw_config["bot"]["admin_id"],  
            api_id=raw_config["bot"]["api_id"],  
            api_hash=raw_config["bot"]["api_hash"],                      
        ),
        db=DatabaseConfig(
            table_id=raw_config["database"]["table_id"],
            cred_file=raw_config["database"]["cred_file"],
            g_drive_media_folder=raw_config["database"]["g_drive_media_folder"],
        ),
        contacts=ContactsConfig(
            common_chanel=raw_config["contacts"]["common_chanel"],
            admin_chanel=raw_config["contacts"]["admin_chanel"],
            admin_chanel_id=raw_config["contacts"]["admin_chanel_id"],
        ),
    )
