from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import settings

import asyncio

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
