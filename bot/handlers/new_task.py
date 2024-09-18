from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.database import session_factory
from db.queries import insert_task

router = Router()

class NewTask(StatesGroup):
    task_text = State()
    task_due = State()

@router.message(Command('new'))
async def cmd_new_text(msg:Message, state:FSMContext):
    await msg.answer("Write your task's text")
    await state.set_state(NewTask.task_text)

@router.message(NewTask.task_text)
async def cmd_new_due(msg:Message, state:FSMContext):
    await state.update_data(task_text = msg.text)
    await msg.answer("Write your task's due date (year-month-day, example: 2024-09-21))")
    await state.set_state(NewTask.task_due)

@router.message(NewTask.task_due)
async def cmd_new_end(msg:Message, state:FSMContext):
    await state.update_data(task_due = datetime.strptime(msg.text, "%Y-%m-%d"))
    user_data = await state.get_data()
    async with session_factory() as session:
        await insert_task(session, user_data['task_text'], user_data['task_due'], msg.from_user.id)
    await msg.answer("Your task is recorded. You can see your task with /list")
    await state.clear()
    