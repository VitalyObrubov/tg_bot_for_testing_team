from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from typing import Union

from app.globals import tgUser, User, bot
from app.handlers.registration.answers import *
from app.handlers.registration.messages import *
from app.handlers.keyboard import make_keyboard
from app.utils import is_email, is_mak


"""
Структура данных по окончании регистрации
'tg_user': tgUser(), 
'approval': 'Согласен', 
'phone': '+79190385728', 
'fio': 'freffere', 
'email': 'erwr@jjji.err', 
'have_tvbox': 'Да', 
'tvbox_model': 'PS7105', 
'mrf': 'MOS', 
'san': '1234234', 
'mak': '00:29:15:80:4E:4A'}
"""


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

 

async def registration_stop(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = make_keyboard(START,"usual",1)
    await message.answer(REGISTRATION_CANCELED, reply_markup=keyboard)

async def registration_start(message: types.Message, state: FSMContext, tg_user: tgUser):
    await RegOrder.start.set()
    tg_user = tgUser(message.from_user)
    # Если пользователь новый проверяем есть ли у него в Телеграмм имя пользователя
    if tg_user.username == None:
        await message.answer(USERNAME_NEEDED)

    await state.update_data(tg_user=tg_user)
    keyboard = make_keyboard(APPROVAL_ANSWERS,"usual",2)
    await message.answer(WELCOME, reply_markup=keyboard)
    await RegOrder.next()

async def registration_approval(message: types.Message, state: FSMContext):
    if message.text == APPROVAL_ANSWERS["yes"]: # В этом поле хранится согласие
        await state.update_data(approval=message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Отправить телефонный номер", request_contact=True))
        keyboard.add(types.KeyboardButton(text=CANCEL["cancel"]))
        await message.answer(ASK_PHONE, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == APPROVAL_ANSWERS["no"]: # В этом поле хранится отказ
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)


async def registration_phone(message: Union[types.Message, types.Contact], state: FSMContext):
    if message.contact != None: # Был прислан контакт
        await state.update_data(phone=message.contact.phone_number)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_FIO, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == CANCEL["cancel"]: # Отказались отправить телефон
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)
        return

async def registration_fio(message: types.Message, state: FSMContext):
    if message.text == CANCEL["cancel"]:
        await registration_stop(message, state)
    else:
        await state.update_data(fio=message.text)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_EMAIL, reply_markup=keyboard)
        await RegOrder.next()

async def registration_email(message: types.Message, state: FSMContext):
    email = is_email(message.text)
    if message.text == CANCEL["cancel"]: # решили прервать регистрацию
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
    if message.text == YES_NO["yes"]: # В этом поле хранится согласие
        await state.update_data(have_tvbox=message.text)
        keyboard = make_keyboard(TV_BOXES,"usual",5)
        await message.answer(ASK_MODEL, reply_markup=keyboard)
        await RegOrder.next()
    elif message.text == YES_NO["no"]: # В этом поле хранится отказ
        await message.answer(ANSW_NOBOX)
        await registration_stop(message, state)
    else:
        await message.answer(ASK_REENTER)

async def registration_model(message: types.Message, state: FSMContext):
    if message.text == TV_BOXES["other"]: # Выбрано другое
        await message.answer(ANSW_BADMODEL)
        await registration_stop(message, state)
    elif message.text in list(TV_BOXES.values()): # введеная модель есть в списке
        await state.update_data(tvbox_model=message.text)
        keyboard = make_keyboard(MRF,"usual",3)
        await message.answer(ASK_MRF, reply_markup=keyboard)
        await RegOrder.next()
    else:
        await message.answer(ASK_REENTER)

async def registration_mrf(message: types.Message, state: FSMContext):
    if message.text == MRF["cancel"]: 
        await registration_stop(message, state)
    elif message.text in  list(MRF.values()): # введеная модель есть в списке
        await state.update_data(mrf=message.text)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_SAN, reply_markup=keyboard)
        await RegOrder.next()
    else:
        await message.answer(ASK_REENTER)

async def registration_subscriber(message: types.Message, state: FSMContext):
    if message.text == CANCEL["cancel"]:
        await registration_stop(message, state)
    else:
        await state.update_data(san=message.text)
        keyboard = make_keyboard(EMPTY,"usual",1)
        await message.answer(ASK_MAK, reply_markup=keyboard)
        await RegOrder.next()

async def registration_mak(message: types.Message, state: FSMContext):
    if message.text == CANCEL["cancel"]: # решили прервать регистрацию
        await registration_stop(message, state)
    elif not(is_mak(message.text)): # ввели неверный mak
        await message.answer(BAD_MAK)
        return 
    else: # ввели верный mac
        await state.update_data(mak=message.text)
        # создаем пользователя и заносим его в базу и текущий список бота
        user_data = await state.get_data()
        user = User()
        user.user_from_reg_data(user_data)
        user.row_num = await bot.database.write_user_to_db(user, bot) # заносим пользователя в базу
        bot.users[user.tg_id] = user
        # отправляем в чат админов сообщение о новом пользователе
        await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, "Добавлен пользователь\n" + str(user))
        # финальные сообщения
        keyboard = make_keyboard(START,"usual",1)
        await message.answer(FIN_MESS.format(user.id), reply_markup=keyboard)
        await message.answer(FIN_MESS2.format(bot.config.contacts.common_chanel), reply_markup=keyboard)
        await state.finish()



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

    