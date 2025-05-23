from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class TestProgress(StatesGroup):
    question_ind = State()
    answers = State()
    correct_answers = State()

    messages_to_delete = State()