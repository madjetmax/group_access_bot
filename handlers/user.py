from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import user as kbs
from states import user as states
from config import *

router = Router()

async def delete_messages(bot: Bot, chat_id: int, messages_ids: list):
    await bot.delete_messages(
        chat_id, message_ids=messages_ids
    )

@router.message(CommandStart(), F.chat.type=="private")
async def start(message: Message, state: FSMContext):
    # send rules
    await message.answer(GREAT)

    # send start test
    kb = kbs.get_start_test()
    msg = await message.answer(START_TEST_MESSAGE_TEXT, reply_markup=kb)

    state_data = await state.get_data()
    messages_to_delete = state_data.get("messages_to_delete")

    if messages_to_delete:
        await delete_messages(message.bot, message.chat.id, messages_to_delete)

    await state.set_state(states.TestProgress)

    await state.update_data(
        question_ind=0,
        answers=0,
        correct_answers=0,
        messages_to_delete=[msg.message_id]
    )

@router.message(Command(commands=["rules"]), F.chat.type=="private")
async def get_rules(message: Message):
    await message.answer(RULES)

@router.message(Command(commands=["help"]), F.chat.type=="private")
async def get_help(message: Message):
    await message.answer(HEPL_COMMAND_TEXT)