from aiogram import Bot, Dispatcher

from bot.handlers.gpt_handlers import gpt_router
from bot.handlers.admin_handlers import admin_router

from database.database_connection import connect_database

from config.config import settings

import logging
import asyncio

# Включите логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

dp.include_router(gpt_router)
dp.include_router(admin_router)

# Запуск бота
async def main():
    await connect_database()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
