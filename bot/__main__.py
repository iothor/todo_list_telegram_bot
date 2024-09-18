import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import bot_settings
from bot.handlers import commands, new_task, update_task

logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher()

    bot = Bot(
        token=bot_settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp.include_router(commands.router)
    dp.include_router(new_task.router)
    dp.include_router(update_task.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
