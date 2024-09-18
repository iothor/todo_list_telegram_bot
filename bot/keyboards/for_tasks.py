from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class TaskCallbackData(CallbackData, prefix = 'task'):
    action: str
    id: int

def default_task_buttons(done: bool, id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Done" if not done else "Not done", callback_data=TaskCallbackData(action="done", id=id))
    kb.button(text="Update", callback_data = TaskCallbackData(action="update", id=id))
    kb.button(text="Delete", callback_data = TaskCallbackData(action="delete", id=id))
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
