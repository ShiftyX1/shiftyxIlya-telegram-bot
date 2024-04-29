from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import settings

import asyncio
import logging

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello!")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Это комманда /help")

@dp.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer("Все хорошо!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход")