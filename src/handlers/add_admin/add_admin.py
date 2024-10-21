from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, admins, bot
from states import States


@dp.callback_query_handler(text='yes', state=States.add_admin)
async def add_admin(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    preview = data.get('preview')

    new_admin = {
        'name': data['name'],
        'id': data['tg_id'],
        'main admin': False
    }

    admins.insert_one(new_admin)

    await query.answer(f"Добавил админа {data['name']}")
    await bot.delete_message(query.message.chat.id, preview)
    await state.set_state(None)



