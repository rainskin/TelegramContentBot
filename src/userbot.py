import asyncio
from datetime import datetime, timedelta
from typing import Any, Iterable, cast, Union

import pyrogram
from pyrogram import errors
from pyrogram.enums import ParseMode
from pyrogram.raw.functions.messages.forward_messages import ForwardMessages
from pyrogram.raw.functions.messages import DeleteScheduledMessages
from pyrogram.raw.types import (
    UpdateNewChannelMessage,
    UpdateNewMessage,
    UpdateNewScheduledMessage,
)
from pyrogram.types import Message
from pyrogram.types.list import List
from pyrogram.utils import datetime_to_timestamp

import config
import loader


class Client(pyrogram.Client):
    def __init__(self, session_string: str, no_updates: bool):
        super().__init__('userbot', session_string=session_string, no_updates=no_updates)  # type: ignore

    async def forward_messages(
            self,
            chat_id: int | str,
            from_chat_id: int | str,
            message_ids: int | Iterable[int],
            disable_notification: bool | None = None,
            schedule_date: datetime | None = None,
            protect_content: bool | None = None,
            drop_author: bool | None = None,
    ) -> Message | list[Message]:

        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]
        r: Any = await self.invoke(  # type: ignore
            ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),  # type: ignore
                from_peer=await self.resolve_peer(from_chat_id),  # type: ignore
                id=message_ids,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                drop_author=drop_author,
            )
        )
        forwarded_messages: list[Message] = []
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        _types = UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage
        for i in r.updates:
            if isinstance(i, _types):
                m = await Message._parse(self, i.message, users, chats)  # type: ignore
                forwarded_messages.append(cast(Message, m))
        return List(forwarded_messages) if is_iterable else forwarded_messages[0]

    async def delete_scheduled_messages(self, chat_id: int, msg_ids):
        await self.invoke(DeleteScheduledMessages(peer=await self.resolve_peer(chat_id), id=msg_ids))


class Userbot:

    def __init__(self):
        self.app = Client(session_string=config.USERBOT_SESSION_STRING, no_updates=True)

    async def send_message(self, chat_id: int | str, text: str):
        try:
            await self.app.start()
        except ConnectionError:
            pass
        await self.app.send_message(chat_id, text, parse_mode=ParseMode.HTML)

    async def copy(self, chat_id, date):
        app = self.app
        try:
            await app.start()
        except ConnectionError:
            pass

        random_msg = await loader.content_collection.aggregate(
            [{"$match": {"channel_id": chat_id}}, {"$sample": {"size": 1}}]).next()
        msg_id = random_msg['msg_id']
        msg = await app.get_messages(config.UPLOAD_CHANNEL_ID, msg_id)

        caption = await get_caption(chat_id)
        print('Caption:', caption)
        if caption:

            msg_caption = msg.caption if msg.caption else ''
            caption = msg_caption + caption
            print(caption)
        else:
            print('No caption')
        try:
            # Для альбомов

            await app.copy_media_group(chat_id=chat_id, from_chat_id=config.UPLOAD_CHANNEL_ID, message_id=msg_id,
                                       captions=caption, schedule_date=date)
        except ValueError:
            # Для соло пикч
            print('try copy message')

            await app.copy_message(chat_id=chat_id, from_chat_id=config.UPLOAD_CHANNEL_ID, message_id=msg_id,
                                   caption=caption,
                                   schedule_date=date)

        print('successfully copied')

        await loader.content_collection.delete_one({'msg_id': msg_id})
        print('deleted from db')


userbot = Userbot()


async def get_caption(chat_id: int):
    doc = await loader.channels.find_one({'id': chat_id})
    return doc.get('caption')
