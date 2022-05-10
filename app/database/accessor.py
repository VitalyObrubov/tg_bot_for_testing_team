import re
import gspread  # импортируем библиотеку
from app.globals import Bot, User



def setup_db(bot: Bot) -> None:
    gs = gspread.service_account(filename=bot.config.db.cred_file)  # подключаем файл с ключами и пр.    
    g_table = gs.open_by_key(bot.config.db.table_id)  # подключаем таблицу по ID
    bot.users_db = g_table.sheet1  # получаем лист 1 там хранятся пользователи
    

async def load_users(bot: Bot):
    bot.users = {}
    data = bot.users_db.get_all_values()
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

def get_row_from_range(range: str) -> int:
    return int(re.findall(r'^\D*(\d+)', range)[0])

def write_user_to_db(user: User, bot: Bot) -> int:
    data_to_write = []
    data_to_write.append(user.tg_id)
    data_to_write.append(f'=HYPERLINK("https://t.me/{user.tg_username}"; "@{user.tg_username}")')
    data_to_write.append(user.id)
    data_to_write.append(user.fullname)
    data_to_write.append(user.phone)
    data_to_write.append(user.email)
    data_to_write.append(user.stb_model)
    data_to_write.append(user.mrf)
    data_to_write.append(user.san)
    data_to_write.append(user.mak)
    res = bot.users_db.append_row(data_to_write, value_input_option = "USER_ENTERED")
    row_num = get_row_from_range(res['updates']['updatedRange'])
    return row_num


