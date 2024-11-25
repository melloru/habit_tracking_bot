import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from middlewares.db import DataBaseSession

from common.bot_cmds_list import private
from handlers.user_private import user_private_router



bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Инициализация бота

dp = Dispatcher() # Отвечает за фильтрацию сообщений(событий)

dp.include_router(user_private_router)

async def on_start_up(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Бот лег')


async def main():
    dp.startup.register(on_start_up)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True) # Сброс обновлений за время АФК бота
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) # Бесконечно спрашивает сервер телеграмм о наличии новых сообщений


if __name__ == '__main__':
    asyncio.run(main()) # Запуск бота
