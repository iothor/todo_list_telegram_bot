from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.database import session_factory
from db.queries import select_tasks_by_user, select_task_by_id, delete_task, update_task

from bot.keyboards.for_tasks import default_task_buttons, TaskCallbackData

router = Router()

class UpdateTask(StatesGroup):
    update_text = State()
    update_due = State()

@router.message(Command('list'))
async def cmd_list(msg:Message):
    async with session_factory() as session:
        tasks = await select_tasks_by_user(session, msg.from_user.id)
    
    for task in tasks:
        answer = f"{task.text}\n"\
                 f"Due: {task.due.date()}\n"\
                 f"{'Done' if task.done else 'Not done'}"
        await msg.answer(answer, reply_markup=default_task_buttons(task.done, task.id))

@router.callback_query(TaskCallbackData.filter(F.action=="done"))
async def btn_done(callback: CallbackQuery, callback_data:TaskCallbackData):
    async with session_factory() as session:
        task = await select_task_by_id(session, callback_data.id)
        task.done = not task.done

        answer = f"{task.text}\n"\
                 f"Due: {task.due.date()}\n"\
                 f"{'Done' if task.done else 'Not done'}"
        await callback.message.edit_text(
            answer, 
            reply_markup=default_task_buttons(task.done, task.id)
        )

        await session.commit()
    await callback.answer()

@router.callback_query(TaskCallbackData.filter(F.action=="delete"))
async def btn_delete(callback: CallbackQuery, callback_data:TaskCallbackData):
    async with session_factory() as session:
        await delete_task(session, callback_data.id)
    await callback.message.delete()
    await callback.message.answer("Task was deleted")
    await callback.answer()

@router.callback_query(TaskCallbackData.filter(F.action=="update"))
async def btn_update_text(callback: CallbackQuery, callback_data:TaskCallbackData, state:FSMContext):
    async with session_factory() as session:
        task = await select_task_by_id(session, callback_data.id)
    await callback.message.answer(f"Old text: {task.text}\nWrite new text for your task")
    await state.set_state(UpdateTask.update_text)
    await state.update_data(task = task)
    await callback.answer()

@router.message(UpdateTask.update_text)
async def btn_update_due(msg:Message, state:FSMContext):
    user_data = await state.get_data()
    await msg.answer(f"Old due: {user_data['task'].due}\nWrite new due date")
    await state.update_data(task_text = msg.text)
    await state.set_state(UpdateTask.update_due)

@router.message(UpdateTask.update_due)
async def btn_update_end(msg:Message, state:FSMContext):
    user_data = await state.get_data()
    async with session_factory() as session:
        await update_task(
            session, 
            user_data['task'].id, 
            user_data['task_text'], 
            datetime.strptime(msg.text, "%Y-%m-%d"), 
            user_data['task'].done
            )
    await msg.answer("Your task was succesfully updated. You can see your task with /list")
