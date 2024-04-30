from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from models.gpt_models import History
from tortoise.exceptions import DoesNotExist

from config.config import settings

import json

admin_router = Router()


@admin_router.message(Command("get_history"))
async def check_history(message: Message, command: CommandObject):

    if message.from_user.id != int(settings.ADMIN_ID):
        await message.reply(text="Вы не являетесь админом :(")
        return None
    
    user_id: str = command.args

    try:
        gpt_history = await History.get(user_id=user_id)

        if gpt_history.historyjson == [] or gpt_history.historyjson == None:
            await message.reply(text=f"История пользователя с таким user_id ({user_id}) пуста!")
            return None
            
        with open(f'files/history_gpt/{user_id}.json', 'w', encoding="utf-8") as f:
            json.dump(gpt_history.historyjson, f)

        json_history = FSInputFile(f'files/history_gpt/{user_id}.json')

        await message.reply_document(document=json_history)
    except DoesNotExist:
        await message.reply(text=f"История пользователя с таким user_id ({user_id}) не найдена!")
