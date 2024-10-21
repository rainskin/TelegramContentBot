import motor.motor_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import userbot

db_client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGO_URL)
db = db_client[config.MONGO_DB_NAME]
admins = db['admins']
channels = db['channels']

other_channels = db['content']
content_collection = other_channels

bot = Bot(token=config.BOT_TOKEN, parse_mode='html', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())
userbot = userbot.Userbot()
