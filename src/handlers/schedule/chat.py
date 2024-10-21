from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import texts
from core import db
from loader import bot, dp, channels
from states import States


@dp.callback_query_handler(state=States.schedule)
async def chose_category(query: types.CallbackQuery, state: FSMContext):
    channel_id = int(query.data)
    channel = await db.channels.get_channel_by_id(channel_id)
    channel_name = channel['title']

    await state.update_data({'channel_name': channel_name, 'channel_id': channel_id})
    await bot.send_message(query.message.chat.id, f'Ты выбрал канал <b>{channel_name}</b>',
                           parse_mode='html')
    await bot.send_message(query.message.chat.id, text=texts.choosing_days,
                           parse_mode=types.ParseMode.MARKDOWN)
    await query.answer()
    await States.choosing_days.set()
