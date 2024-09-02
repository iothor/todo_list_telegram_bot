import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import bot_settings

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

bot = Bot(
    token=bot_settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
