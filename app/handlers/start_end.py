from xmlrpc.client import Boolean
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


from app.handlers.registration.dataclassess import tgUser

from app.handlers.registration.messages import USERNAME_NEEDED
from app.handlers.registration.hendlers import register_handlers_registration, registration_start

def new_user(tg_user: tgUser) -> Boolean:
    return True


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    tg_user = tgUser(message.from_user)
    if new_user(tg_user):
        if tg_user.username == None:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("/start")
            await message.answer(USERNAME_NEEDED, reply_markup=keyboard)
        else:
            await registration_start(message, state, tg_user)
    else:
        pass


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    await message.answer("Действие отменено", reply_markup=keyboard)

async def any_text_message(message: types.Message, state: FSMContext):
    await cmd_start(message, state)




def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")

    register_handlers_registration(dp)
    
    # Этот обработчик обязательно должен быть последним
    dp.register_message_handler(any_text_message)

