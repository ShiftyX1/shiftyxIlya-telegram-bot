from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import g4f
import g4f.Provider
import random


gpt_router = Router()

# Словарь для хранения истории разговоров
conversation_history = {}

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
    conversation_history[user_id] = []
    await message.reply("История диалога очищена.")

# Обработчик для каждого нового сообщения
@gpt_router.business_message()
async def send_welcome(message: Message):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])

    chat_history = conversation_history[user_id]

    providers = [g4f.Provider.Feedough, g4f.Provider.FreeGpt]

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=providers[random.randint(0, 1)]
        )
        chat_gpt_response = response
    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(conversation_history)
    length = sum(len(message["content"]) for message in conversation_history[user_id])
    print(length)
    await message.answer(f"{chat_gpt_response}")

