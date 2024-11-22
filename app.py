import os

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import load_dotenv
load_dotenv()


bot = Bot(token=os.getenv('TOKEN')) # Инициализация бота

dp = Dispatcher() # Отвечает за фильтрацию сообщений(событий)


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(message.text)


@dp.message()
async def start_cmd(message: types.Message):
    await message.answer(message.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True) # Сброс обновлений за время АФК бота
    await dp.start_polling(bot) # Бесконечно спрашивает сервер телеграмм о наличии новых сообщений

asyncio.run(main()) # Запуск бота
