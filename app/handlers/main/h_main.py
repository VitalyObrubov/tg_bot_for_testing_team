from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.globals import User, bot
from app.handlers.main.answers import *
from app.handlers.main.messages import *
from app.handlers.main.h_info import InfoOrder, register_handlers_info, info_start
from app.handlers.keyboard import make_keyboard
from app.database.g_disk import upload_files


class MainOrder(StatesGroup):
    # Состояния по которым идет диалог
    start = State()
    waiting_for_main_command = State()
    waiting_for_input_info = State()


async def main_start(message: types.Message, state: FSMContext):
    await state.finish()
    await MainOrder.start.set()
    keyboard = make_keyboard(MAIN_MENU,"usual",2)
    await message.answer(MAIN_WELCOME, reply_markup=keyboard)
    await MainOrder.waiting_for_main_command.set()

async def handle_main_command(message: types.Message, state: FSMContext):
    await state.update_data(mess_text=[])
    await state.update_data(files={})
    if message.text == MAIN_MENU["problems"]: 
        await state.update_data(request_type="problems")
        keyboard = make_keyboard(SEND_PROBLEM,"usual",2)
        await message.answer(ASK_PROBLEM, reply_markup=keyboard)
        await MainOrder.waiting_for_input_info.set()
    
    elif message.text == MAIN_MENU["ideas"]:
        await state.update_data(request_type="ideas")
        keyboard = make_keyboard(SEND_IDEA,"usual",2)
        await message.answer(ASK_IDEA, reply_markup=keyboard)
        await MainOrder.waiting_for_input_info.set()
    
    elif message.text == MAIN_MENU["questions"]:
        await state.update_data(request_type="questions") 
        keyboard = make_keyboard(SEND_QUESTION,"usual",2)
        await message.answer(ASK_QUESTION, reply_markup=keyboard)
        await MainOrder.waiting_for_input_info.set()
    
    elif message.text == MAIN_MENU["check"]: 
        await message.answer(CHECK_MESS)
    
    elif message.text == MAIN_MENU["info"]: 
        await info_start(message, state)
    
    else:
        await message.answer(ASK_REENTER)

async def handle_input_info(message: types.Message, state: FSMContext):
    tg_user_id = message.from_user.id
    user = bot.users.get(message.from_user.id)
    if message.text == CANCEL_INPUT:
        pass # Сюда не доходит перехватывается раньше
    if message.text in [SEND_PROBLEM["send"],SEND_IDEA["send"],SEND_QUESTION["send"]]:
        user_data = await state.get_data()
        file_links = await upload_files(user_data["files"])
        mess = {}
        mess["file_links"] = ", ".join(file_links)
        mess["text"] = ", ".join(user_data["mess_text"])
        mess["request_type"] = user_data["request_type"]
        mess_id = await bot.database.write_user_request(user, bot, mess) # заносим сообщение в базу
        # отправляем в чат админов сообщение о новом пользователе
        await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, 
                                    TO_ADMIN_NEW[mess["request_type"]].format(mess_id) 
                                    + user.main_info() + "\n" + mess["text"] + 
                                    "\n" + mess["file_links"])
        for file_id in user_data["files"]:
            file = await bot.aiobot.get_file(file_id)
            if file.file_path.startswith("photos"):                
                await bot.aiobot.send_photo(bot.config.contacts.admin_chanel_id,file_id)
            elif file.file_path.startswith("videos"):                
                await bot.aiobot.send_video(bot.config.contacts.admin_chanel_id,file_id)
            elif file.file_path.startswith("documents"):                
                await bot.aiobot.send_document(bot.config.contacts.admin_chanel_id,file_id)
            elif file.file_path.startswith("music"):                
                await bot.aiobot.send_audio(bot.config.contacts.admin_chanel_id,file_id)
        await message.answer(MESSAGE_SENDED)
        await main_start(message, state)

    else:
        str_tg_id = str(tg_user_id)
        files = state.storage.data[str_tg_id][str_tg_id]['data']['files']    
        if message.text != None:
            state.storage.data[str_tg_id][str_tg_id]['data']['mess_text'].append(message.text)
        if message.document != None:
            files[message.document.file_id] = message.document.file_name
        if (message.photo != None) and (len(message.photo)>0):    
            files[message.photo[-1].file_id] = "noname.jpg"
        if message.video != None:    
            files[message.video.file_id] = message.video.file_name
        if message.audio != None:    
            files[message.audio.file_id] = message.audio.file_name


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(main_start, state=InfoOrder.waiting_for_info_command, text = INFO_MENU["main_menu"])
    dp.register_message_handler(main_start, state=MainOrder.waiting_for_input_info, text = CANCEL_INPUT)
    dp.register_message_handler(handle_main_command, state=MainOrder.waiting_for_main_command)
    dp.register_message_handler(handle_input_info, state=MainOrder.waiting_for_input_info,content_types=types.ContentType.ANY)

    register_handlers_info(dp)

    