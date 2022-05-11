import logging
from typing import Optional, Dict, List, Any
from aiogram import Bot as aioBot, Dispatcher
from dataclasses import dataclass
from aiogram.types.user import User as aioUser

from config.config_reader import Config
#from app.database.accessor import GoogleDatabase


class Bot():
    config: Optional[Config] = None
    aiobot: Optional[aioBot] = None # непосредственно сам бот aiogram 
    dp: Optional[Dispatcher] = None # его диспетчер
    logger: Optional[logging.Logger] = None  # логгер
    database: Any = None # менеджер доступа к аккаунту google
    users: Dict[int, "User"] = {} # пользователи



#//////////////////////////////////////

bot = Bot() # Самый главный объект всего приложения

#//////////////////////////////////////


 # данные пользователя которые можно взять из Телеграм
@dataclass
class tgUser:
    def __init__(self, user: aioUser):
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.full_name = user.full_name
        self.url = user.url

 # непосредственно наш пользователь
class User:
    row_num: int
    tg_id: int
    tg_username: str
    id: int
    fullname: str
    phone: str
    email: str
    stb_model: str
    mrf: str
    san: str
    mak: str

    def __str__(self):
        res = f"Телеграм ИД - {self.tg_id}\n"
        res += f"Телеграм имя - {self.tg_username}\n"
        res += f"ИД - <b>{self.id}</b>\n"
        res += f"ФИО - {self.fullname}\n"
        res += f"Телефон - {self.phone}\n"
        res += f"e-mail - {self.email}\n"
        res += f"Модель приставки - {self.stb_model}\n"
        res += f"MRF - {self.mrf}\n"
        res += f"SAN - {self.san}\n"
        res += f"MAK - {self.mak}\n"
        return res

    def main_info(self):
        res = f"ИД - <b>{self.id}</b>\n"
        res += f"{self.tg_username}\n"
        res += f"MRF - {self.mrf}\n"
        res += f"MAK - {self.mak}\n"
        return res

    def user_from_g_table(self, data: List):
        if len(data) < 10:
            return False
        self.tg_id = int(data[0])
        self.tg_username = data[1]
        self.id = int(data[2])
        self.fullname = data[3]
        self.phone = data[4]
        self.email = data[5]
        self.stb_model = data[6]
        self.mrf = data[7]
        self.san = data[8]
        self.mak = data[9]
        return True

 
    """
    Структура данных по окончании регистрации
    'tg_user': tgUser(), 
    'approval': 'Согласен', 
    'phone': '+79190385728', 
    'fio': 'freffere', 
    'email': 'erwr@jjji.err', 
    'have_tvbox': 'Да', 
    'tvbox_model': 'PS7105', 
    'mrf': 'MOS', 
    'san': '1234234', 
    'mak': '00:29:15:80:4E:4A'}
    """
    def user_from_reg_data(self, data: Dict):
        self.tg_id = int(data["tg_user"].id)
        self.tg_username = f"@{data['tg_user'].username}"
        self.id = 0
        self.fullname = data["fio"]
        self.phone = data["phone"]
        self.email = data["email"]
        self.stb_model = data["tvbox_model"]
        self.mrf = data["mrf"]
        self.san = data["san"]
        self.mak = data["mak"]