import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv, find_dotenv

import message_router  # тот самый роутер

load_dotenv(find_dotenv())


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(message_router.router)  # тут добавляем наши роутеры
    await dp.start_polling(bot)


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # получаем токен бота из переменной окружения
    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN is not set")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())