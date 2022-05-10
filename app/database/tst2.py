import asyncio

import gspread_asyncio

# from google-auth package
from google.oauth2.service_account import Credentials 

# First, set up a callback function that fetches our credentials off the disk.
# gspread_asyncio needs this to re-authenticate when credentials expire.

def get_creds():
    # To obtain a service account JSON file, follow these steps:
    # https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account
    creds = Credentials.from_service_account_file("gsheetscred.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped

# Create an AsyncioGspreadClientManager object which
# will give us access to the Spreadsheet API.

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

# Here's an example of how you use the API:

async def example(agcm):
    # Always authorize first.
    # If you have a long-running program call authorize() repeatedly.
    agc = await agcm.authorize()


    
    sh = await agc.open_by_key('1vybR8raLw_oXvfMb8o8c5cYbPQrmmVQ9QjhaNUJcALQ')  # подключаем таблицу по ID
    
    worksheet = await sh.worksheet("users")  # получаем первый лист
    await worksheet.append_row(["Онищенко", '=HYPERLINK("seyepapeseny@gmail.com";"email")', 220, "+5343466636"],value_input_option = "USER_ENTERED")  # добавить новую строку с данными

  
    print("All done!")

# Turn on debugging if you're new to asyncio!
asyncio.run(example(agcm), debug=True)