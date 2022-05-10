from xmlrpc.client import Boolean
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


from app.globals import tgUser
from app.globals import bot

from app.handlers.registration.messages import USERNAME_NEEDED
from app.handlers.registration.hendlers import register_handlers_registration, registration_start

def new_user(tg_user: tgUser) -> Boolean:
    user = bot.users.get(tg_user.id)
    return user == None # если пользователь не найден то он новый


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    tg_user = tgUser(message.from_user)
    if new_user(tg_user):
        # Если пользователь новый проверяем есть ли у него в Телеграмм имя пользователя и идем в ветку регистрации 
        if tg_user.username == None:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("/start")
            await message.answer(USERNAME_NEEDED, reply_markup=keyboard)
        else:
            await registration_start(message, state, tg_user)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("/start")
        await message.answer("Поздравляю вы зарегистрированный пользователь", reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    await message.answer("Действие отменено", reply_markup=keyboard)

async def any_text_message(message: types.Message, state: FSMContext):
    await cmd_start(message, state)

async def cmd_reload_users(message: types.Message):
    from app.database.accessor import load_users
    if message.from_user.id == bot.config.bot.admin_id:
        await load_users(bot)
        await message.answer("Пользователи перезагружены")
    else:
        await message.answer("Недостаточно прав")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_reload_users, commands="reload_users", state="*", chat_type=types.ChatType.PRIVATE)

    register_handlers_registration(dp)
    
    # Этот обработчик обязательно должен быть последним
    dp.register_message_handler(any_text_message, chat_type=types.ChatType.PRIVATE)

