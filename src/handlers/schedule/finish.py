import asyncio
from datetime import datetime
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot, content_collection
from loader import userbot
from states import States
from utils.time import create_valid_date, one_day, get_current_datetime


@dp.callback_query_handler(state=States.accept)
async def finish(query: types.CallbackQuery, state: FSMContext):
    if query.data != 'accept':
        return

    data = await state.get_data()
    channel_name = str(data['channel_name'])
    channel_id = data['channel_id']
    days = data['days']
    time = data['time']

    current_datetime = get_current_datetime()
    current_day = current_datetime['day']
    current_month = current_datetime['month']
    current_year = current_datetime['year']

    first_date = create_valid_date(days[0], current_day, current_month, current_year)

    if len(days) == 2:
        second_date = create_valid_date(days[1], current_day, current_month, current_year) or first_date
    else:
        second_date = first_date

    date = first_date

    search_parameter = channel_id

    total_photos_count = await content_collection.count_documents({'channel_id': search_parameter})
    amount_of_days = second_date.day - first_date.day + 1
    requested_posts_count = amount_of_days * len(time) - calculate_dropped_posts(first_date, time)

    if requested_posts_count > total_photos_count:
        await bot.send_message(query.message.chat.id,
                               f'В коллекции *{total_photos_count}* ты запросил {requested_posts_count}\nПополни '
                               f'коллекцию, либо выбери другие даты',
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(query.message.chat.id, 'Начинаю планирование постов')
        await query.answer()
        while date <= second_date:
            try:
                await schedule_posts(date, time, channel_name, channel_id)
            except Exception as e:
                await query.message.answer(f'что-то пошло не так\n\n{e}')
                break

            date += one_day
            await asyncio.sleep(2)

        await bot.send_message(query.message.chat.id, 'Готово')

    await state.finish()


async def schedule_posts(date: datetime, time: list, channel_name: str, channel_id: int):
    year = date.year
    month = date.month
    day = date.day

    current_datetime = get_current_datetime()
    current_day = current_datetime['day']
    current_hour = current_datetime['hour']

    search_parameter = 'url'  # for tyan and vip tyan
    for hour in time:

        if date.day == current_day and current_hour > hour:
            continue

        minute = randint(0, 8)
        schedule_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        await userbot.copy(channel_id, schedule_date)

        await asyncio.sleep(0.1)


def calculate_dropped_posts(date: datetime, time: list[int]):
    current_datetime = get_current_datetime()
    current_day = current_datetime['day']
    current_hour = current_datetime['hour']
    dropped_posts = 0

    for hour in time:
        if date.day == current_day and current_hour > hour:
            dropped_posts += 1

    return dropped_posts
