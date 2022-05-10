import re
from time import sleep
from gspread_asyncio import AsyncioGspreadWorksheet, AsyncioGspreadClientManager
from google.oauth2.service_account import Credentials 

from app.globals import Bot, User


class GoogleDatabase:
    manager: AsyncioGspreadClientManager
   
    def __init__(self, bot: Bot):
        def get_creds():
            creds = Credentials.from_service_account_file(bot.config.db.cred_file)
            scoped = creds.with_scopes([
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ])
            return scoped
        self.manager = AsyncioGspreadClientManager(get_creds)
        

    async def get_g_sheets(self, bot: Bot, sheets_names: list) -> dict: # получает из таблицы лист по имени
        agc = await self.manager.authorize()
        sh = await agc.open_by_key(bot.config.db.table_id)  # подключаем таблицу по ID
        worksheets = {}
        for sheet_name in sheets_names:
            worksheets[sheet_name] = await sh.worksheet(sheet_name)
        return worksheets

    async def load_users(self, bot: Bot):
        sheets = await self.get_g_sheets(bot, ["users"])   
        users_db = sheets["users"]
        bot.users = {}
        data = await users_db.get_all_values()
        row = 2
        err_rows = ""
        bot.max_id = 100
        for g_user in data[1:]: # читаем со второй сроки, в первой имена столбцов
            user = User()
            if not user.user_from_g_table(g_user):
                err_rows += row+", "
            else:
                user.row_num = row
                bot.users[user.tg_id] = user
            row += 1
            bot.max_id = max(bot.max_id, user.id)
            
        if len(err_rows) > 0:
            mess = "Ошибка загрузки пользователей в строках " + err_rows
            await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, mess)

    def get_row_from_range(self, range: str) -> int:
        return int(re.findall(r'^\D*(\d+)', range)[0])

    def get_range_hyperlink(self, bot: Bot, sheet: AsyncioGspreadWorksheet, range: str) -> int:
        return f"https://docs.google.com/spreadsheets/d/{bot.config.db.table_id}/edit#gid={sheet.id}&range={range}:{range}"
        
    async def write_user_to_db(self, user: User, bot: Bot) -> int:
        data_to_write = []
        data_to_write.append(user.tg_id)
        data_to_write.append(f'=HYPERLINK("https://t.me/{user.tg_username}"; "{user.tg_username}")')
        data_to_write.append(user.id)
        data_to_write.append(user.fullname)
        data_to_write.append(user.phone)
        data_to_write.append(user.email)
        data_to_write.append(user.stb_model)
        data_to_write.append(user.mrf)
        data_to_write.append(user.san)
        data_to_write.append(user.mak)
        
        sheets = await self.get_g_sheets(bot, ["users"])   
        users_db = sheets["users"]
        res = await users_db.append_row(data_to_write, value_input_option = "USER_ENTERED")
        row_num = self.get_row_from_range(res['updates']['updatedRange'])
        return row_num

    async def write_user_change_request(self, user: User, bot: Bot, mess: str) -> int:
        data_to_write = []
        sheets = await self.get_g_sheets(bot, ["change_user_data_requests","users"])
        requests_db = sheets["change_user_data_requests"]
        uswers_db = sheets["users"]
        userlink = self.get_range_hyperlink(bot,uswers_db, user.row_num)
        data_to_write.append(f'=HYPERLINK("{userlink}"; "{user.id}")')
        data_to_write.append(f'=HYPERLINK("https://t.me/{user.tg_username}"; "{user.tg_username}")')
        data_to_write.append(mess)
        res = await requests_db.append_row(data_to_write, value_input_option = "USER_ENTERED")
        row_num = self.get_row_from_range(res['updates']['updatedRange'])
        return row_num        


