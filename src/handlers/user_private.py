from aiogram.types import Message
from aiogram import  types, Bot, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from src.kbds import reply_buttons, inline_buttons
import src.handlers.worker as worker

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: Message,state:FSMContext,bot:Bot) -> None:
    await message.answer("Здравствуйте, воспользуйтесь клавиатурой ниже",reply_markup=reply_buttons.get_keyboard(
                    "часто задаваемые вопросы","новости туластата","о нас",
                    sizes=(1,1,1)
                ))
    j = message.message_id
    print(j)
    await state.update_data(message_id=j)

@user_private_router.message(F.text == "часто задаваемые вопросы")
async def questions(message: Message,bot:Bot,state:FSMContext) -> None:
    message_str = ''
    i = 1
    inline_kb=InlineKeyboardBuilder()
    for elem in worker.get_questions():
        message_str += str(i) + ') '
        message_str += elem
        message_str += '\n'
        inline_kb.add(InlineKeyboardButton(text=f"Вопрос {i}",callback_data=f"question_{i}"))
        i += 1
    
    await message.answer(text=message_str,reply_markup=inline_kb.adjust(4,4,4,4,1).as_markup())

@user_private_router.callback_query(F.data.startswith("question_"))
async def question_select(callback:types.CallbackQuery, bot:Bot, ):
    que_id=callback.data.split("_")[-1]
    i = 1
    for elem in worker.get_answers():
        if int(que_id) == i:
            print(i, que_id)
            await bot.edit_message_text(text = elem, chat_id= callback.message.chat.id, message_id=callback.message.message_id)
            await bot.edit_message_reply_markup(chat_id= callback.message.chat.id, message_id=callback.message.message_id,reply_markup=inline_buttons.get_callback_btns(butns={
                    "назад":"back_"
                }))
        i += 1

@user_private_router.callback_query(F.data.startswith("back_"))
async def question_select(callback:types.CallbackQuery, bot:Bot, ):
            await bot.edit_message_text(text = "Выберите действие на клавиатуре ниже", chat_id= callback.message.chat.id, message_id=callback.message.message_id)
            await bot.edit_message_reply_markup(reply_markup=reply_buttons.get_keyboard(
                    "часто задаваемые вопросы","новости туластата","о нас",
                    sizes=(1,1,1)
                ), chat_id= callback.message.chat.id, message_id=callback.message.message_id)

@user_private_router.message(F.text == "новости туластата")
async def news(message: Message,bot:Bot,state:FSMContext) -> None:
    
    i=0
    news = worker.get_news(i)
    print(news)
    await message.answer(text=news,reply_markup=inline_buttons.get_callback_btns(
        butns={
            'следующая новость':f'next_{i+1}',
            "назад":"back_"
        }
    ))

@user_private_router.callback_query(F.data.startswith("next_"))
async def news_select_next(callback:types.CallbackQuery, bot:Bot, ):
    news_id=int(callback.data.split("_")[-1])
    news = worker.get_news(news_id)
    await bot.edit_message_text(text = news, chat_id= callback.message.chat.id, message_id=callback.message.message_id)
    await bot.edit_message_reply_markup(chat_id= callback.message.chat.id, message_id=callback.message.message_id,reply_markup=inline_buttons.get_callback_btns(butns={
        'следующая новость':f'next_{news_id+1}',
        'предыдущая новость':f'previous_{news_id-1}',
        "назад":"back_"
    }))

@user_private_router.callback_query(F.data.startswith("previous_"))
async def news_select_back(callback:types.CallbackQuery, bot:Bot, ):
    news_id=int(callback.data.split("_")[-1])
    news = worker.get_news(news_id)
    await bot.edit_message_text(text = news, chat_id= callback.message.chat.id, message_id=callback.message.message_id)
    if news_id > 0:
        await bot.edit_message_reply_markup(chat_id= callback.message.chat.id, message_id=callback.message.message_id,reply_markup=inline_buttons.get_callback_btns(butns={
            'следующая новость':f'next_{news_id+1}',
            'предыдущая новость':f'previous_{news_id-1}',
            "назад":"back_"
        }))
    else:
        await bot.edit_message_reply_markup(chat_id= callback.message.chat.id, message_id=callback.message.message_id,reply_markup=inline_buttons.get_callback_btns(butns={
            'следующая новость':f'next_{news_id+1}',
            "назад":"back_"
        }))

@user_private_router.message(F.text == "о нас")
async def info(message: Message,bot:Bot,state:FSMContext) -> None:

    await message.answer(text='Наш сайт: https://rosstat.gov.ru/ \n\n ')