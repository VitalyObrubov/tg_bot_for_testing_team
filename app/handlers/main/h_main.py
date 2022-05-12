from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.globals import User, bot
from app.handlers.main.answers import *
from app.handlers.main.messages import *
from app.handlers.main.h_info import InfoOrder, register_handlers_info, info_start
from app.handlers.keyboard import make_keyboard


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
    user = bot.users.get(message.from_user.id)
    if message.text == CANCEL_INPUT:
        pass # Сюда не доходит перехватывается раньше
    if message.text in [SEND_PROBLEM["send"],SEND_IDEA["send"],SEND_QUESTION["send"]]:
        await message.answer(MESSAGE_SENDING)
        user_data = await state.get_data()
        dir_id = None
        if len(user_data["files"]):
            dir_id = await bot.g_drive.upload_files(user, user_data["files"],user_data["request_type"])
        dir_link = "https://drive.google.com/drive/folders/" + dir_id
        mess = {}
        mess["file_links"] = dir_link
        mess["text"] = ", ".join(user_data["mess_text"])
        mess["request_type"] = user_data["request_type"]
        mess_id = await bot.database.write_user_request(user, bot, mess) # заносим сообщение в базу
        if dir_id: # Если директория с файлами была создана, меняем ее имя
            bot.g_drive.change_folder_name(dir_id, str(mess_id))
        # отправляем в чат админов сообщение о новом пользователе
        await bot.aiobot.send_message(bot.config.contacts.admin_chanel_id, 
                                    TO_ADMIN_NEW[mess["request_type"]].format(mess_id) 
                                    + user.main_info() + "\n" + mess["text"] + 
                                    "\n" + mess["file_links"])
        files = user_data["files"]
        for file_id in files:
            file = await bot.aiobot.get_file(file_id)
            caption = files[file_id]["caption"]
            if file.file_path.startswith("photos"):                
                await bot.aiobot.send_photo(chat_id=bot.config.contacts.admin_chanel_id,photo=file_id,caption=caption)
            elif file.file_path.startswith("videos"):                
                await bot.aiobot.send_video(chat_id=bot.config.contacts.admin_chanel_id,video=file_id,caption=caption)
            elif file.file_path.startswith("documents"):                
                await bot.aiobot.send_document(chat_id=bot.config.contacts.admin_chanel_id,document=file_id,caption=caption)
            elif file.file_path.startswith("music"):                
                await bot.aiobot.send_audio(chat_id=bot.config.contacts.admin_chanel_id,audio=file_id,caption=caption)
        await message.answer(MESSAGE_SENDED)
        await main_start(message, state)

    else:
        big_file = False
        MB20 = 20480000
        user_data = await state.get_data()
        files = user_data['files'] 
        mess_text = user_data['mess_text']     
        if message.text != None:
            mess_text.append(message.text)
        elif message.caption != None:
            mess_text.append(message.caption)
        if message.document != None:
            big_file = (message.document.file_size > MB20)
            files[message.document.file_id] = {"name": message.document.file_name,"caption": message.caption}
        if (message.photo != None) and (len(message.photo)>0):
            big_file = (message.photo[-1].file_size > MB20)    
            files[message.photo[-1].file_id] = {"name": "photo","caption": message.caption}
        if message.video != None:
            big_file = (message.video.file_size > MB20)    
            files[message.video.file_id] = {"name": message.video.file_name,"caption": message.caption}
        if message.audio != None:
            big_file = (message.audio.file_size > MB20)    
            files[message.audio.file_id] = {"name": message.audio.file_name,"caption": message.caption}
        if big_file:
            await message.answer(BIG_FILE)
        else:
            await state.update_data(files=files)
        await state.update_data(mess_text=mess_text)

def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(main_start, state=InfoOrder.waiting_for_info_command, text = INFO_MENU["main_menu"])
    dp.register_message_handler(main_start, state=MainOrder.waiting_for_input_info, text = CANCEL_INPUT)
    dp.register_message_handler(handle_main_command, state=MainOrder.waiting_for_main_command)
    dp.register_message_handler(handle_input_info, state=MainOrder.waiting_for_input_info,content_types=types.ContentType.ANY)

    register_handlers_info(dp)

    