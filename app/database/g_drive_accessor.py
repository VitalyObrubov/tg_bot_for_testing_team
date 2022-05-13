import os
import asyncio
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import Resource, build
from app.globals import User, Bot, bot

class GoogleDrive:
    service: Resource
    credentials: service_account.Credentials
    def __init__(self, bot: Bot):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = bot.config.db.cred_file
        self.credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    def init(self):
        self.service = build('drive', 'v3', credentials = self.credentials)

    async def upload_file_to_g_dive(self, file_metadata, media):
        self.service.files().create(body=file_metadata, media_body=media).execute() 

    async def upload_to_g_dive(self, path: str, request_type: str):
        self.init()

        # Поиск папки по типу запроса
        media_folder_id = bot.config.db.g_drive_media_folder
        q_text = f"mimeType = 'application/vnd.google-apps.folder' and name = '{request_type}' and '{media_folder_id}' in parents"
        request_folders = self.service.files().list(
            fields = "nextPageToken, files(id)",
            q = q_text
            ).execute()
        if len(request_folders['files']) == 0:
            name = request_type
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [media_folder_id]
            }
            request_folder = self.service.files().create(body=file_metadata, fields='id').execute()
            request_folder_id = request_folder["id"]
        else:
            request_folder_id = request_folders['files'][0]["id"]

        # Создаем папку сообщения
        name = request_type
        file_metadata = {
            'name': "NewMessage",  # потом переименуем по ид сообщения
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [request_folder_id]
        }
        mess_folder = self.service.files().create(body=file_metadata, fields='id').execute()        
        mess_folder_id = mess_folder["id"] 

        # грузим файлы на Google Drive
        files = os.listdir(path)
        for file in files:
            file_metadata = {'name': file, 'parents': [mess_folder_id]}
            media = MediaFileUpload(os.path.join(path, file), resumable=True)
            upload_task = asyncio.create_task(self.upload_file_to_g_dive(file_metadata, media)) 
            await upload_task       
        return mess_folder_id

    def change_folder_name(self, dir_id: str, name: str):
        body = { "name": name }
        self.service.files().update(fileId=dir_id, body=body).execute()


    async def upload_files(self, user: User, files: dict, request_type: str) -> str: 
        # возвращает ид папки на Гугл диске куда сложены файлы
        # скачивает файлы с Телеграма затем вызывает метод их закачки на Гугл диск 
        path = os.path.join('media',str(user.id))
        if not os.path.exists(path):
            os.mkdir(path)

        for file_id in files:
            file = await bot.aiobot.get_file(file_id)
            file_path = file.file_path
            filename = files[file_id]["name"]
            if filename == "photo":
                filename = file.file_path.split("/")[-1]
            dest_file = os.path.join(path, filename)
            await bot.aiobot.download_file(file_path, dest_file)

        dir_id = await self.upload_to_g_dive(path, request_type)
        # del files
        files = os.listdir(path)
        for file in files:
            os.remove(os.path.join(path, file))
        os.rmdir(path)    

        return dir_id