from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from loader import dp, bot
from states import States


@dp.callback_query_handler(state=States.choosing_time)
async def choosing_time(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    time = [int(i) for i in data.split(', ')]

    await state.update_data(time=time)
    await query.message.delete()
    await bot.send_message(query.message.chat.id, f'Ты выбрал следующие временные слоты:\n{time}',
                           reply_markup=keyboards.finish_schedule_kb)
    await States.accept.set()

@dp.message_handler(state=States.choosing_time)
async def _(msg: types.Message, state: FSMContext):
    try:
        time: List[int] = [int(i) for i in msg.text.split(' ')]
    except TypeError as e:
        await msg.answer("Неверный формат, введи числа без запятой, например [11 15 23]")
        return

    for i in time:
        if is_not_correct_hours_amount(i):
            await msg.answer(f"Некорректно указано время: {i}")
            return

    await bot.send_message(msg.from_user.id, f'Ты выбрал следующие временные слоты:\n{time}',
                           reply_markup=keyboards.finish_schedule_kb)
    await States.accept.set()



def is_not_correct_hours_amount(hours: int):
    return hours < 0 or hours > 23