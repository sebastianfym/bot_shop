import asyncio
import io
import logging

import os
import sys

from aiogram.fsm.storage.memory import MemoryStorage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_bot.telegram_bot.settings')

import django
django.setup()
from telegram_bot.accounts.models import User


import aiohttp
from aiogram.types import KeyboardButton
from django.db.models import Q
from datetime import datetime
from aiogram import Bot, Dispatcher, types

# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.filters import Text
# from aiogram.utils.exceptions import BadRequest
# from datetime import datetime
# from aiogram.dispatcher import FSMContext


from config import BASE_URL, bot

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["/start", "старт", "start"])
async def start(message: types.Message):
    telegram_id = message.from_user.id
    # try:
    #
    # except ObjectDoesNotExist:
    user = User.objects.get(telegram_id=int(telegram_id))

    if telegram_id != None:

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="Главное меню"))

        await message.answer("Вы в главном меню", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(KeyboardButton(text="продолжить"))
        await message.answer('Привет, ', reply_markup=keyboard)



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())