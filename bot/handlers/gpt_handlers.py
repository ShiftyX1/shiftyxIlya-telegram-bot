from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from models.gpt_models import History
from tortoise.exceptions import DoesNotExist

import g4f
import g4f.Provider
import random
import json


gpt_router = Router()
gpt_answers_if_not_text = ["Упс! По всей видимости вы отправили картинку/гифку/стикер/документ и т.д, к сожалению, на данном этапе разработки я умею обрабатывать только текст, но в скором времени это планируется исправить!"]


def history_to_json(history_dict: dict) -> str:
    """
    Конвертируем историю сообщений в строку JSON для последующей вставки в PostgreSQL
    """
    return json.dumps(history_dict)

# Функция для обрезки истории разговора
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


@gpt_router.business_message(Command('clear'))
async def process_clear_command(message: Message):
    user_id = message.from_user.id
    try:
        history = await History.get(user_id=user_id)
        
        if history.historyjson == []:
            await message.reply("По всей видимости ранее вы уже очищали историю диалога, очистка не требуется")
            return None
        
        history.historyjson = history_to_json([])
        await history.save()
        await message.reply("История диалога очищена.")
    except DoesNotExist:
        await message.reply("Вы еще не общались с ChatGPT в рамках этого чата. История отсутствует.")

# Обработчик для каждого нового сообщения к GPT
@gpt_router.business_message()
async def gpt_response(message: Message):
    if message.content_type == ContentType.TEXT:
        user_id = message.from_user.id
        user_input = message.text

        historydb_query = await History.get_or_create(user_id=str(user_id))

        if historydb_query[0].historyjson == None:
            historydb_query[0].historyjson = history_to_json([])
            await historydb_query[0].save()

        conversation_history = await History.get(user_id=str(user_id))
        chat_history = conversation_history.historyjson
        chat_history.append({"role": "user", "content": user_input})

        # conversation_history[user_id] = trim_history(conversation_history[user_id])
        #chat_history = conversation_history[user_id]

        providers = [g4f.Provider.Feedough]

        try:
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.default,
                messages=chat_history,
                provider=providers[0]
            )
            chat_gpt_response = response
        except Exception as e:
            print(f"{g4f.Provider.GeekGpt.__name__}:", e)
            chat_gpt_response = "Извините, произошла ошибка."

        chat_history.append({"role": "assistant", "content": chat_gpt_response})
        conversation_history.historyjson = json.dumps(chat_history)
        await conversation_history.save()

        #print(conversation_history.historyjson.encode(encoding="utf-8"))
        #length = sum(len(message["content"]) for message in conversation_history[user_id])
        #print(length)

        await message.answer(f"{chat_gpt_response}")
    else:
        await message.answer(gpt_answers_if_not_text[0])

