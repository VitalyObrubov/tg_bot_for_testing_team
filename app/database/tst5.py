from telethon import TelegramClient

api_id = 15051227
api_hash = '5f8599d664e1839e95c942b5d4e550e6'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    async for message in client.iter_messages("asinc_t_bot", 10):
        print(message.id, message.text)
        if message.photo:
            print('File Name :' + str(message.file.name))
            path = await client.download_media(message.media, "youranypathhere")
            print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())

