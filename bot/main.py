import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.task_bot.handlers import register_handlers
from bot.task_bot.middlewares import DjangoMiddleware
from bot.task_bot.config import BOT_TOKEN, API_URL

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    dp.middleware.setup(DjangoMiddleware(API_URL))
    register_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())