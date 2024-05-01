from aiogram.fsm.state import State, StatesGroup

class GPTChat(StatesGroup):
    chat_with_gpt = State()


class DefaultStates(StatesGroup):
    default_state = State()
    waiting_for_command = State()