from telethon import TelegramClient
from telethon.tl.functions.messages import GetMessagesRequest

api_id = 15051227
api_hash = '5f8599d664e1839e95c942b5d4e550e6'
token = "5226131452:AAHrKRcpvv-4s2Uzyvfxk4i65fvBCDj2JrQ"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=token)
async def main():
    result = await client(GetMessagesRequest(id=[2210]))    
    message = result.messages[0]
    print('File Name :' + str(message.file.name))
    path = await message.download_media(message.media, "youranypathhere")
    print('File saved to', path)  # printed after download is done
    
with client:
    client.loop.run_until_complete(main())

async def rrrr(): # так можно вставить в основной код
    from telethon import TelegramClient
    from telethon.tl.functions.messages import GetMessagesRequest

    api_id = 15051227
    api_hash = '5f8599d664e1839e95c942b5d4e550e6'
    token = "5226131452:AAHrKRcpvv-4s2Uzyvfxk4i65fvBCDj2JrQ"
    client = await TelegramClient('bot', api_id, api_hash).start(bot_token=token)
    result = await client(GetMessagesRequest(id=[2210]))    
    messag = result.messages[0]
    path = await messag.download_media()
    print('File saved to', path)  # printed after download is done

