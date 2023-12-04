from aiogram import Bot
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

bot = Bot(token=os.getenv("BOT_TOKEN"))

logger.add("all_logs.log", rotation="500 MB", level="INFO")