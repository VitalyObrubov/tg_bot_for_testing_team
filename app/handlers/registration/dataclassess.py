from dataclasses import dataclass
from aiogram.types.user import User as aioUser

@dataclass
class tgUser:
    def __init__(self, user: "aioUser"):
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.full_name = user.full_name
        self.url = user.url
        self.phone = None




