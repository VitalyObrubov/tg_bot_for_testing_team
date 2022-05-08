from cgitb import text
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from typing import Union

from app.globals import bot
from app.handlers.registration.answers import *
from app.handlers.registration.messages import *
from app.handlers.registration.dataclassess import tgUser
from app.handlers.keyboard import make_keyboard
from app.utils import is_email, is_mak



class RegOrder(StatesGroup):
    # Состояния по которым идет диалог
    start = State()
    waiting_for_approval = State()
    waiting_for_phone = State()
    waiting_for_fio = State()
    waiting_for_email = State()
    waiting_for_tv = State()
    waiting_for_model = State()
    waiting_for_mrf = State()
    waiting_for_subscr = State()
    waiting_for_mak = State()
    waiting_for_fin = State()
 


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
        keyboard = make_keyboard(EMPTY,"usual",1)
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
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_EMAIL, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await RegOrder.next()

async def registration_email(message: types.Message, state: FSMContext):
    email = is_email(message.text)
    if message.text == CANCEL[0]: # решили прервать регистрацию
        await registration_stop(message, state)
    elif not(email): # ввели неверный email
        await message.answer(BAD_EMAIL)
        return 
    else: # ввели верный email
        await state.update_data(email=email)
        keyboard = make_keyboard(YES_NO,"usual",2)
        await message.answer(ASK_TV, reply_markup=keyboard)
        await RegOrder.next()

async def registration_tv(message: types.Message, state: FSMContext):
    if message.text == YES_NO[0]: # В этом поле хранится согласие
        await state.update_data(have_tvbox=message.text)
        keyboard = make_keyboard(TV_BOXES,"usual",5)
        await message.answer(ASK_MODEL, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == YES_NO[1]: # В этом поле хранится отказ
        await message.answer(ANSW_NOBOX)
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)

async def registration_model(message: types.Message, state: FSMContext):
    if message.text == TV_BOXES[-1]: # Выбрано другое
        await message.answer(ANSW_BADMODEL)
        await registration_stop(message, state)
    elif message.text in TV_BOXES: # введеная модель есть в списке
        await state.update_data(tvbox_model=message.text)
        keyboard = make_keyboard(MRF,"usual",3)
        await message.answer(ASK_MRF, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await RegOrder.next()
    else:
        await message.answer(ASK_REENTER)

async def registration_mrf(message: types.Message, state: FSMContext):
    if message.text == MRF[-1]: # Выбрано другое
        await registration_stop(message, state)
    elif message.text in MRF: # введеная модель есть в списке
        await state.update_data(mrf=message.text)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_SUBSCRIBER, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await RegOrder.next()
    else:
        await message.answer(ASK_REENTER)

async def registration_subscriber(message: types.Message, state: FSMContext):
    if message.text == CANCEL[0]:
        await registration_stop(message, state)
    else:
        await state.update_data(subscr_id=message.text)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_MAK, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await RegOrder.next()

async def registration_mak(message: types.Message, state: FSMContext):
    if message.text == CANCEL[0]: # решили прервать регистрацию
        await registration_stop(message, state)
    elif not(is_mak(message.text)): # ввели неверный mak
        await message.answer(BAD_MAK)
        return 
    else: # ввели верный mac
        await state.update_data(mac=message.text)
        keyboard = make_keyboard(OK,"usual",2)
        await message.answer(FIN_MESS.format(123456), reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await message.answer(FIN_MESS2.format(bot.config.contacts.common_chanel), reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        await RegOrder.next()

async def registration_finish(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, str(user_data))
    from app.handlers.start_end import cmd_start
    await cmd_start(message, state)


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(registration_approval, state=RegOrder.waiting_for_approval)
    dp.register_message_handler(registration_phone, content_types=["contact","text"], state=RegOrder.waiting_for_phone)
    dp.register_message_handler(registration_fio, state=RegOrder.waiting_for_fio)
    dp.register_message_handler(registration_email, state=RegOrder.waiting_for_email)
    dp.register_message_handler(registration_tv, state=RegOrder.waiting_for_tv)
    dp.register_message_handler(registration_model, state=RegOrder.waiting_for_model)
    dp.register_message_handler(registration_mrf, state=RegOrder.waiting_for_mrf)
    dp.register_message_handler(registration_subscriber, state=RegOrder.waiting_for_subscr)
    dp.register_message_handler(registration_mak, state=RegOrder.waiting_for_mak)
    dp.register_message_handler(registration_finish, state=RegOrder.waiting_for_fin)
    