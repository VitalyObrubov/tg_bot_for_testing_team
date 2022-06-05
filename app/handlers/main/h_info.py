from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.globals import User, bot
from app.handlers.main.answers import *
from app.handlers.main.messages import *
from app.handlers.keyboard import make_keyboard

class InfoOrder(StatesGroup):
    # Состояния по которым идет диалог
    start = State()
    waiting_for_info_command = State()
    waiting_for_user_info = State()
    waiting_for_change_info = State()


async def info_start(message: types.Message, state: FSMContext):
    await InfoOrder.start.set()
    keyboard = make_keyboard(INFO_MENU,"usual",2)
    await message.answer(INFO_WELCOME, reply_markup=keyboard)
    await InfoOrder.waiting_for_info_command.set()

async def handle_info_command(message: types.Message, state: FSMContext):
    if message.text == INFO_MENU["my_data"]: 
        user = bot.users.get(message.from_user.id)
        keyboard = make_keyboard(CHANGE_USER_DATA,"usual",2)
        await message.answer(str(user), reply_markup=keyboard)
        await InfoOrder.waiting_for_user_info.set()
    elif message.text == INFO_MENU["howto"]: 
        await message.answer(HOWTO_MESS)
    elif message.text == INFO_MENU["q&a"]: 
        await message.answer(QA_MESS)
    elif message.text == INFO_MENU["digests"]: 
        await message.answer(DIGESTS_MESS)
    elif message.text == INFO_MENU["main_menu"]: 
        pass # Сюда не доходит перехватывается раньше
    else:
        await message.answer(ASK_REENTER)

async def handle_user_info(message: types.Message, state: FSMContext):
    if message.text == CHANGE_USER_DATA["change"]: 
        keyboard = make_keyboard(CANCEL,"usual",2)
        await message.answer(CHANGE_USER_INFO_MESS, reply_markup=keyboard)
        await InfoOrder.waiting_for_change_info.set()
    elif message.text == CHANGE_USER_DATA["back"]: 
        pass # Сюда не доходит перехватывается раньше
    else:
        await message.answer(ASK_REENTER)

async def handle_change_user_info(message: types.Message, state: FSMContext):
    user = bot.users.get(message.from_user.id)
    mess = {}
    mess["request_type"] = "change_user_data"    
    mess["text"] = message.text
    mess["file_links"] = ""

    await message.answer(USER_IFO_REQUEST_SEND)
    await info_start(message, state)
    
    mess_id = await bot.database.write_user_request(user, bot, mess) # заносим сообщение в базу

    # отправляем в чат админов сообщение о новом пользователе
    await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, 
                                  TO_ADMIN_USER_CHANGE_INFO.format(mess_id) 
                                  + user.main_info() + "\n" + message.text)

def register_handlers_info(dp: Dispatcher):
    dp.register_message_handler(info_start, state=InfoOrder.waiting_for_user_info, text = CHANGE_USER_DATA["back"])
    dp.register_message_handler(info_start, state=InfoOrder.waiting_for_change_info, text = CANCEL["cancel"])
    dp.register_message_handler(handle_info_command, state=InfoOrder.waiting_for_info_command)
    dp.register_message_handler(handle_user_info, state=InfoOrder.waiting_for_user_info)
    dp.register_message_handler(handle_change_user_info, state=InfoOrder.waiting_for_change_info)