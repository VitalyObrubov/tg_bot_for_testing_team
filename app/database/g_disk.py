from app.globals import bot

async def upload_files(files: dict) -> list: # возвращает список ссылок на файлы
    links = []
    for file_id in files:
        file = await bot.aiobot.get_file(file_id)
        file_path = file.file_path
        res = await bot.aiobot.download_file(file_path,"media/"+file_path)
        links.append("media/"+file_path)
    return links