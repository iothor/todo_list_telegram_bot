from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.database import session_factory
from db.queries import insert_user, select_users


router = Router()

@router.message(Command("start"))
async def cmd_start(msg: Message):
    answer = \
    "This is todo list telegram bot. You can track your task with this bot.\n" \
    "Available commands: /start, /help, /list, /new"

    async with session_factory() as session:
        users = await select_users(session)
        user_ids = [u.id for u in users]
        if msg.from_user.id not in user_ids:
            await insert_user(session, msg.from_user.id, msg.from_user.username)
            await msg.answer("We added you to our database where we save all your tasks")

    await msg.answer(answer)


@router.message(Command("help"))
async def cmd_help(msg: Message):
    answer = \
    "This is todo list telegram bot. You can track your task with this bot.\n" \
    "Available commands: /start, /help, /list, /new"


    await msg.answer(answer)
