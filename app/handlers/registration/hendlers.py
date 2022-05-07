from cgitb import text
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from typing import Union

from app.handlers.registration.answers import *
from app.handlers.registration.messages import *
from app.handlers.registration.dataclassess import tgUser
from app.handlers.keyboard import make_keyboard
from app.utils import is_email


class RegOrder(StatesGroup):
    start = State()
    waiting_for_approval = State()
    waiting_for_phone = State()
    waiting_for_fio = State()
    waiting_for_email = State()
    waiting_for_tv = State()


async def registration_stop(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/start")
    await message.answer(REGISTRATION_CANCELED, reply_markup=keyboard)

async def registration_start(message: types.Message, state: FSMContext, tg_user: tgUser):
    await RegOrder.start.set()
    await state.update_data(tg_user=tg_user)
    keyboard = make_keyboard(APPROVAL_ANSWERS,"usual",2)
    await message.answer(WELCOME, reply_markup=keyboard)
    await RegOrder.next()

async def registration_approval(message: types.Message, state: FSMContext):
    if message.text == APPROVAL_ANSWERS[0]: # В этом поле хранится согласие
        await state.update_data(approval=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Отправить телефонный номер", request_contact=True))
        keyboard.add(types.KeyboardButton(text=CANCEL[0]))
        await message.answer(ASK_PHONE, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == APPROVAL_ANSWERS[1]: # В этом поле хранится отказ
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)


async def registration_phone(message: Union[types.Message, types.Contact], state: FSMContext):
    if message.contact != None: # Был прислан контакт
        await state.update_data(phone=message.contact.phone_number)
        keyboard = make_keyboard(CANCEL,"usual",1)
        await message.answer(ASK_FIO, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == CANCEL[0]: # Отказались отправить телефон
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)
        return

async def registration_fio(message: types.Message, state: FSMContext):
    if message.text == CANCEL[0]:
        await registration_stop(message, state)
    else:
        await state.update_data(fio=message.text)
        keyboard = make_keyboard(CANCEL,"usual",1)
        await message.answer(ASK_EMAIL, reply_markup=keyboard)
        await RegOrder.next()

async def registration_email(message: types.Message, state: FSMContext):
    if message.text == CANCEL[0]: # решили прервать регистрацию
        await registration_stop(message, state)
    elif not(is_email(message.text)): # ввели неверный email
        await message.answer(BAD_EMAIL)
        return 
    else: # ввели верный email
        await state.update_data(email=message.text)
        keyboard = make_keyboard(YES_NO,"usual",2)
        await message.answer(ASK_TV, reply_markup=keyboard)
        await RegOrder.next()

async def registration_tv(message: types.Message, state: FSMContext):
    pass

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(registration_approval, state=RegOrder.waiting_for_approval)
    dp.register_message_handler(registration_phone, content_types=["contact","text"], state=RegOrder.waiting_for_phone)
    dp.register_message_handler(registration_fio, state=RegOrder.waiting_for_fio)
    dp.register_message_handler(registration_email, state=RegOrder.waiting_for_email)
    dp.register_message_handler(registration_tv, state=RegOrder.waiting_for_tv)