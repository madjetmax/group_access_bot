from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards import user as kbs
from keyboards import filters
from states import user as states 

from config import *
import asyncio

import datetime


router = Router()


def get_question_data(ind) -> dict | None:
    if ind >= len(ALL_QUESTIONS):
        return None
    question = ALL_QUESTIONS[ind]
    return question

@router.callback_query(F.data == "start_test")
async def start_test(call: CallbackQuery, state: FSMContext):
    if call.message.chat.type == "private":
        message: Message = call.message

        new_question = get_question_data(0)
        text, kb = kbs.get_question(new_question, 0)

        msg = await message.answer(
            text, 
            reply_markup=kb
        )

        # setting state
        state_data = await state.get_data()

        if state_data == {}:
            await state.set_state(states.TestProgress)
            await state.update_data(
                question_ind=0,
                answers=0,
                correct_answers=0,
                messages_to_delete=[msg.message_id]
            )
        else:
            messages_to_delete = state_data["messages_to_delete"]
            messages_to_delete.append(msg.message_id)
            state_data = await state.get_data()

            await state.update_data(messages_to_delete=messages_to_delete)

        await call.answer("")

async def delete_messages(bot: Bot, chat_id: int, messages_ids: list):
    await bot.delete_messages(
        chat_id, message_ids=messages_ids
    )

async def generate_group_link(bot: Bot) -> str:
    expire_date=datetime.timedelta(minutes=GROP_LINK_LIFE_TIME)

    link = await bot.create_chat_invite_link(
        GROUP_ID, 
        member_limit=1,
        expire_date=expire_date
    )

    return link.invite_link

@router.callback_query(filters.Answer.filter())
async def check_answer(call: CallbackQuery, callback_data: filters.Answer, state: FSMContext):
    if call.message.chat.type == "private":
        message: Message = call.message

        question_ind = callback_data.question_ind
        answer_correct: bool = callback_data.is_correct

        state_data = await state.get_data()

        if state_data != {}: # check state is not empty
            messages_to_delete = state_data["messages_to_delete"]

            if answer_correct: # update state and send new question
                # update state
                await state.update_data(question_ind=question_ind+1)
                if answer_correct:
                    correct_answers_count = state_data["correct_answers"]
                    await state.update_data(correct_answers=correct_answers_count+1)

                # next question
                new_question = get_question_data(question_ind+1)
                if new_question:
                    text, kb = kbs.get_question(new_question, question_ind+1)

                    msg = await message.answer(
                        text, 
                        reply_markup=kb
                    )
                    messages_to_delete.append(msg.message_id)
                    state_data = await state.get_data()
        
                    await state.update_data(messages_to_delete=messages_to_delete)
                else:
                    # send link
                    state_data = await state.get_data()
                    correct_answers_count = state_data["correct_answers"]

                    if correct_answers_count == len(ALL_QUESTIONS):
                        link = await generate_group_link(message.bot)
                        kb = kbs.get_group_link(link)
                        await message.answer(LINK_LIFETIME_TEXT, reply_markup=kb)
                        await state.clear()

                        await delete_messages(message.bot, call.message.chat.id, messages_to_delete)

            else: # start again from rules and start test button
            
                kb = kbs.get_start_test()
                msg = await message.answer(TEST_FAIL_TEXT, reply_markup=kb)

                await delete_messages(message.bot, call.message.chat.id, messages_to_delete)

                await state.update_data(
                    question_ind=0,
                    answers=0,
                    correct_answers=0,
                    messages_to_delete=[msg.message_id]
                )

        else: # start test if state if empty
            await message.delete()
            kb = kbs.get_start_test()
            await message.answer(START_TEST_MESSAGE_TEXT, reply_markup=kb)

        await call.answer("")
        