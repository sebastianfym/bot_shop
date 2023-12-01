from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

bot = Bot(token=os.getenv("BOT_TOKEN"))