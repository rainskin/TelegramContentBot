from aiogram import types

import keyboards
import texts
from core import db
from core.db import channels
from loader import dp
from states import States


@dp.message_handler(commands='schedule')
async def cmd_schedule(msg: types.Message):
    if not await db.admins.is_superadmin(msg.from_user.id):
        return
    else:
        user_id = msg.from_user.id
        user_channels = await channels.get_channels(user_id)
        await msg.answer(text=texts.schedule_main, reply_markup=keyboards.Channels(user_channels))
        await States.schedule.set()

