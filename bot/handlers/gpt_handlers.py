from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from models.gpt_models import History

from tortoise.exceptions import DoesNotExist

from bot.states.states import GPTChat, DefaultStates

import g4f
import g4f.Provider
import random
import json


gpt_router = Router()
gpt_answers_if_not_text = [
    "",
    "Упс! По всей видимости вы отправили картинку/гифку/стикер/документ и т.д, к сожалению, на данном этапе разработки я умею обрабатывать только текст, но в скором времени это планируется исправить!",
    "К сожалению, пока что я не умею обрабатывать ничего кроме текста :( Но я верю, что в будущем удастся это исправить",
    "除了文字，我什么都不认得 , вам понятны слова выше? Нет? Вот и я не понимаю ничего кроме текста, пожалуйста, отправьте корректный промпт!"
    ]


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


@gpt_router.business_message(StateFilter(DefaultStates.waiting_for_command), Command('gpt_start'))
async def start_gpt_chat(message: Message, state: FSMContext):
    await message.answer(text="Можете общаться с ChatGPT!")
    await state.set_state(GPTChat.chat_with_gpt)


@gpt_router.business_message(StateFilter(GPTChat.chat_with_gpt), Command('cancel_chat'))
async def cancel_gpt_chat(message: Message, state: FSMContext):
    await state.set_state(None)
    await message.answer(text="Чат с ChatGPT остановлен")


@gpt_router.business_message(Command('clear'))
async def process_clear_command(message: Message):
    user_id = message.from_user.id
    try:
        history = await History.get(user_id=user_id)
        
        if history.historyjson == []:
            await message.reply("Ранее вы уже очищали историю диалога, очистка не требуется")
            return None
        
        history.historyjson = history_to_json([])
        await history.save()
        await message.reply("История диалога очищена.")
    except DoesNotExist:
        await message.reply("Вы еще не общались с ChatGPT в рамках этого чата. История отсутствует.")

# Обработчик для каждого нового сообщения к GPT
@gpt_router.business_message(StateFilter(GPTChat.chat_with_gpt))
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

        await message.answer(f"{chat_gpt_response}")
    else:
        await message.answer(gpt_answers_if_not_text[random.randint(1, 3)])

