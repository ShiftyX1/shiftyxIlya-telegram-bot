import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from bot.handlers.gpt_handlers import gpt_router

from config.config import settings

# Включите логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

dp.include_router(gpt_router)

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")
