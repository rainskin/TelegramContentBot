from datetime import datetime as dt, datetime
from typing import List

from core import db
from loader import channels, other_channels, content_collection


def get_ids_of_all_channels() -> List[int]:
    return channels.distinct('id')

async def count_content_posts_by_channel(owner_id: int) -> List[tuple]:
    all_channels = await db.channels.get_channels(owner_id)
    channel_ids = [channel['id'] for channel in all_channels]
    channel_title_and_amount = []

    for channel_id in channel_ids:

        channel = await db.channels.get_channel_by_id(channel_id)
        channel_title = channel['title']

        number_of_posts = await content_collection.count_documents({'channel_id': channel_id})

        channel_title_and_amount.append((channel_title, number_of_posts))

    return channel_title_and_amount
