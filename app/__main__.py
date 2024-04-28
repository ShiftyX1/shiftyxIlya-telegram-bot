import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

API_TOKEN = 'token'


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}. Рад тебя видеть!')
    await message.answer(f'Привет {message.from_user.first_name}. Рад тебя видеть!')



logging.basicConfig(level=logging.INFO)

async def start():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot=bot)

    dp.message.register(get_start)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())

