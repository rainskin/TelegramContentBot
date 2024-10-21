from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
import loader
from loader import dp, bot, channels
from states import States


@dp.callback_query_handler(state=States.upload_channel)
async def upload(query: types.CallbackQuery, state: FSMContext):
    channel_id = int(query.data)
    channel = await channels.find_one({'id': channel_id})
    print(channel)
    channel_name = channel['title']

    total_photos_count = await loader.content_collection.count_documents({'channel_id': channel_id})
    print(total_photos_count)
    await bot.send_message(query.message.chat.id,
                           f'Ты выбрал канал <b>{channel_name}</b>. В базе {total_photos_count} постов')
    await state.update_data(channel_name=channel_name, channel_id=channel_id)
    await bot.send_message(query.message.chat.id,
                           'Отправляй сюда посты, которые хочешь добавить в базу, а потом нажми на кнопку',
                           reply_markup=keyboards.done_kb)
    await States.collect_pictures.set()
