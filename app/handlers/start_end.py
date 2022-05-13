from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from app.globals import tgUser
from app.globals import bot
from app.handlers.registration.hendlers import register_handlers_registration, registration_start
from app.handlers.main.h_main import register_handlers_main, main_start

def new_user(tg_user: tgUser) -> bool:
    user = bot.users.get(tg_user.id)
    return user == None # если пользователь не найден то он новый


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    tg_user = tgUser(message.from_user)
    if new_user(tg_user):
        await registration_start(message, state, tg_user)
    else:
        await main_start(message, state)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    await message.answer("Действие отменено", reply_markup=keyboard)

async def any_text_message(message: types.Message, state: FSMContext):
    await cmd_start(message, state)

async def cmd_reload_users(message: types.Message):
    if message.from_user.id == bot.config.bot.admin_id:
        await bot.database.load_users(bot)
        await message.answer("Пользователи перезагружены")
    else:
        await message.answer("Недостаточно прав")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(cmd_reload_users, commands="reload_users", state="*", chat_type=types.ChatType.PRIVATE)

    register_handlers_registration(dp)
    register_handlers_main(dp)
    
    # Этот обработчик обязательно должен быть последним
    dp.register_message_handler(any_text_message, chat_type=types.ChatType.PRIVATE)

