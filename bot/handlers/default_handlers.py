from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.states.states import DefaultStates
from bot.keyboards.simple_row import make_row_keyboard

from config.config import settings


default_router = Router()


@default_router.business_message(StateFilter(None))
async def empty_chat(message: Message, state: FSMContext):
    await message.answer(
        text="Привет, я ассистент Shifty! Если вы хотите пообщатся с ChatGPT напишите /gpt_start , если моя помощь не нужна, нажмите 'Помощь не нужна'"
        )
    await state.set_state(DefaultStates.waiting_for_command)
    
    
@default_router.business_message(StateFilter(DefaultStates.waiting_for_command), Command('cancel'))
async def cancel_assistant(message: Message, state: FSMContext):
    await message.answer(text="Понял вас, помощь отменена! Напишите /assistant если вдруг понадоблюсь!")
    await state.set_state(DefaultStates.default_state)

@default_router.business_message(StateFilter(DefaultStates.default_state), Command('assistant'))
async def start_assistant(message: Message, state: FSMContext):
    await message.answer(text="Я снова здесь, чем могу помочь?")
    await state.set_state(DefaultStates.waiting_for_command)

    