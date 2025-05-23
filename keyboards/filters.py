from aiogram.filters.callback_data import CallbackData

class Answer(CallbackData, prefix="answer"):
    question_ind: int
    is_correct: bool