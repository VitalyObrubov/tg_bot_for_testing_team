from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build

import pprint
import io

pp = pprint.PrettyPrinter(indent=4)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/home/vitaly/freelance/rt_bot/gsheetscred.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# # Создание папки
# folder_id = '1uuecd6ndiZlj3d9dSVeZeKyEmEkC7qyr'
# name = 'New Folder'
# file_metadata = {
#     'name': name,
#     'mimeType': 'application/vnd.google-apps.folder',
#     'parents': [folder_id]
# }
# # возврат {"id":"ssdgskhirry8345y88wytiuwrtwb"}
# r = service.files().create(body=file_metadata,
#                                     fields='id').execute()
# pp.pprint(r)
# # Загрузка файла
# folder_id = '1mCCK9QGQxLDED8_pgq2dyvkmGRXhWEtJ'
# name = 'Script_2.py'
# file_path = '/home/makarov/Script.py'
# file_metadata = {
#                 'name': name,
#                 'parents': [folder_id]
#             }
# media = MediaFileUpload(file_path, resumable=True)
# # возврат {"id":"ssdgskhirry8345y88wytiuwrtwb"}
# r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
# pp.pprint(r)

# Поиск файла по имени файла
# q="" \
#   "mimeType = 'application/vnd.google-apps.folder'" \
#   " and name = 'questions'"\
#   " and '1aJMLUxXrq8cD5PHc8oIPLZnbj_0vKX7o' in parents"
# results = service.files().list(
#     fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
#     q=q
#     ).execute()

body = { "name": "wwwwwwwww" }
res = service.files().update(fileId="108zJABSLh0CTpPdhqGoy0RnzCpF8bPrm", body=body).execute()

pp.pprint(res)


