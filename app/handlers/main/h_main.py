from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import Union

from app.globals import User, bot
from app.handlers.main.answers import *
from app.handlers.main.messages import *
from app.handlers.main.h_info import InfoOrder, register_handlers_info, info_start
from app.handlers.keyboard import make_keyboard


class MainOrder(StatesGroup):
    # Состояния по которым идет диалог
    start = State()
    waiting_for_main_command = State()


async def main_start(message: types.Message, state: FSMContext):
    await MainOrder.start.set()
    keyboard = make_keyboard(MAIN_MENU,"usual",2)
    await message.answer(MAIN_WELCOME, reply_markup=keyboard)
    await MainOrder.waiting_for_main_command.set()

async def handle_main_command(message: types.Message, state: FSMContext):
    if message.text == MAIN_MENU["problem"]: 
        pass
    elif message.text == MAIN_MENU["idea"]: 
        pass
    elif message.text == MAIN_MENU["question"]: 
        pass
    elif message.text == MAIN_MENU["check"]: 
        pass
    elif message.text == MAIN_MENU["info"]: 
        await info_start(message, state)
    else:
        await message.answer(ASK_REENTER)


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(main_start, state=InfoOrder.waiting_for_info_command, text = INFO_MENU["main_menu"])
    dp.register_message_handler(handle_main_command, state=MainOrder.waiting_for_main_command)

    register_handlers_info(dp)

    