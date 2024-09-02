from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer("Hello!")


@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("Help is here")


@router.message(Command("list"))
async def cmd_list(msg: Message):
    await msg.answer("List of your tasks")


@router.message(Command("new"))
async def cmd_new(msg: Message):
    await msg.answer("You created new task")
