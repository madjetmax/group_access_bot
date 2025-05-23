from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import user as kbs
from states import user as states
from config import *

router = Router()

@router.message(CommandStart(), F.chat.type=="private")
async def start(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data == {}:
        # send rules
        await message.answer(RULES)

        # send start test
        kb = kbs.get_start_test()
        msg = await message.answer(START_TEST_MESSAGE_TEXT, reply_markup=kb)

        await state.set_state(states.TestProgress)

        await state.update_data(
            question_ind=0,
            answers=0,
            correct_answers=0,
            messages_to_delete=[msg.message_id]
        )
    
    else:
        await message.answer(START_TEST_AGAIN_TEXT, reply_markup=None)

@router.message(Command(commands=["rules"]), F.chat.type=="private")
async def get_rules(message: Message):
    await message.answer(RULES)