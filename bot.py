import asyncio
import os

from app.create_bot import setup_bot

async def main():
    # инициализация объектов бота и диспетчера
    conf_file = os.environ.get("SETTINGS_MODULE")
    if not conf_file:
        conf_file = "config.yml"    
    bot = await setup_bot(config_path=os.path.join(os.path.dirname(__file__), conf_file))

    # Запуск поллинга
    await bot.dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    bot.logger.info("Start bot")

    await bot.dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())