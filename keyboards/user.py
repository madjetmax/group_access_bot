from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import *
from . import filters

def get_start_test() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=START_TEST_BUTTON_TEXT, callback_data="start_test")]
    ])

    return kb

def get_question(question, ind):
    text: str = question["text"]
    answers = question["answers"]
    
    kb = InlineKeyboardBuilder()
    for answer in answers:
        call_data = filters.Answer(question_ind=ind, is_correct=answer["correct"]).pack()
        kb.row(
            InlineKeyboardButton(text=answer["text"], callback_data=call_data)
        )

    return (text, kb.as_markup())
    
def get_group_link(link):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=CHAT_BUTTON_TEXT, url=link)]
        ]
    )
    return kb