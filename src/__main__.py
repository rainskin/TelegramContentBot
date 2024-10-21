import asyncio
from pyrogram_patch import patch_pyrogram
from aiogram import executor

import handlers
from loader import dp, bot, userbot
from utils.debug import check_memory_usage, check_task_amount

patch_pyrogram()
handlers.setup()


async def on_startup(dp):
    await userbot.app.start()
    await bot.delete_webhook()

    print('bot started')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup, allowed_updates=[])
