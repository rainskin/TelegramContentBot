from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from core import db
from loader import dp, admins
from states import States


@dp.message_handler(commands='admins')
async def _(msg: types.Message, state: FSMContext):
    if not await db.admins.is_superadmin(msg.from_user.id):
        await msg.answer('Нет доступа')
    else:
        await States.waiting_msg_from_user.set()
        previews_ids = await show_admins(msg)
        await state.update_data(previews_ids=previews_ids)
        await msg.answer(
            f'Текущий список админов. Чтобы добавить нового админа для этого бота, перешли любое сообщение от пользователя, которого хочешь сделать админом')


async def show_admins(msg: types.Message):

    admin_ids = (admins.distinct('id'))
    msg_ids = []
    for _id in admin_ids:
        admin = admins.find_one({'id': _id})
        if admin['main admin']:
            continue

        msg = await msg.answer(f"<b>{admin['name']}</b>\nid: {admin['id']}",
                               parse_mode='html', reply_markup=keyboards.DelAdmin())
        msg_ids.append(msg.message_id)

    return msg_ids


@dp.callback_query_handler(text='delete', state=States.waiting_msg_from_user)
async def _(query: types.CallbackQuery, state: FSMContext):

    text = query.message.text.split('\n')
    admin_name = text[0]
    admin_id = int(text[1][4:])

    admins.delete_one({'id': admin_id})
    await query.answer(f'Удалил админа {admin_name}', show_alert=True)

    data = await state.get_data()
    previews_ids = data['previews_ids']

    msg_id = query.message.message_id
    new_previews_ids = await remove_element_from_data(previews_ids, msg_id)
    await state.update_data(previews_ids=new_previews_ids)

    await query.message.delete()


async def remove_element_from_data(data: list, el):
    for i in data:
        if i == el:
            data.remove(el)
        return data
