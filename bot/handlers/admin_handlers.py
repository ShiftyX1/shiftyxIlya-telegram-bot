from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ParseMode

from models.gpt_models import History

from tortoise.exceptions import DoesNotExist

from config.config import settings

from apps.copypastas.copypasta_parser import random_copypasta

import json

admin_router = Router()


@admin_router.message(Command("get_history"))
async def check_history(message: Message, command: CommandObject):

    if message.from_user.id != int(settings.ADMIN_ID):
        await message.reply(text="Вы не являетесь админом :(")
        return None
    
    user_id: str = command.args
    if user_id == None:
        await message.reply(text="После ввода команды необходимо добавить ID пользоватля. <b>/get_history {id}</b>", parse_mode=ParseMode.HTML)
        return None

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

@admin_router.message(Command('random_pasta'))
async def random_paste(message: Message):
    pasta = await random_copypasta()
    await message.answer(text=pasta)


# TODO: НИЖЕ СДЕЛАН ХЕНДЛЕР ИНЛАЙН РЕЖИМА,
# НУЖНО БУДЕТ С НИМ РАЗОБРАТЬСЯ И ПОДУМАТЬ
# ЧЕМ ОН МОЖЕТ БЫТЬ ПОЛЕЗЕН, 
# пока работает не совсем корректно, по факту я просто спиздил чужой код)) 
# толком с этим функционалом не разбирался((
# -------------------------------------------------
@admin_router.inline_query(F.query == 'pasta')
async def inline_pasta(inline_query: InlineQuery):
    results = []
    pastarandom = await random_copypasta()
    results.append(InlineQueryResultArticle(
            id="id",
            title='Рандомная паста',
            description="Отправить рандомную пасту",
            input_message_content=InputTextMessageContent(
                message_text=pastarandom,
                parse_mode="HTML"
            )
        ))
    await inline_query.answer(results=results, is_personal=True)
