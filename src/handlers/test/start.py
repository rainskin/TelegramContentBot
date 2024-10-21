import re

import pyrogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from pyrogram.storage.sqlite_storage import get_input_peer

import loader
from core import db
from loader import dp, userbot, bot
from states import States


@dp.message_handler(commands='test')
async def cmd_test(msg: types.Message, state: FSMContext):
    if not await db.admins.is_superadmin(msg.from_user.id):
        return

    print('starting')
    coll = loader.db['list_of_channels']
    user_id = msg.from_user.id
    all_channels = coll.find()

    count = 0
    async for channel in all_channels:
        title: str = channel['title']

        if 'тестовый' in title.lower():
            continue

        channel: dict
        channel_id = channel['id']
        channel.pop('_id')
        print(channel)
        if await db.channels.is_unique(channel_id):
            count += 1

            await db.channels.add_channel(user_id, channel)

    print(f'Добавил {count} каналов')
    print('done')


@dp.message_handler(state=States.test, content_types=ContentType.ANY)
async def _(msg: types.Message, state: FSMContext):
    text = replace_emoji_tags(msg.html_text)
    await userbot.send_message('me', text)


def replace_emoji_tags(msg_html_text: str):
    return re.sub(
        r'<tg-emoji emoji-id="(.*?)">(.*?)</tg-emoji>',
        r'<emoji id=\1>\2</emoji>',
        msg_html_text,
    )


# <tg-emoji emoji-id="6152103458209007684">☺️</tg-emoji>


async def get_all_peers(storage):
    # Извлекаем все пиры из базы данных
    peers = storage.conn.execute("SELECT id, access_hash, type FROM peers").fetchall()

    if not peers:
        print("No peers found in storage")
        return []

    return [get_input_peer(*peer) for peer in peers]
