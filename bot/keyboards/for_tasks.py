from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def default_task_buttons() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Done")
    kb.button(text="Update")
    kb.button(text="Delete")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
