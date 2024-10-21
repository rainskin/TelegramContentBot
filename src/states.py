from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):

    # Загрузка контента
    upload_channel = State()
    collect_pictures = State()

    # Отложка
    schedule = State()
    choosing_days = State()
    choosing_time = State()
    accept = State()

    # add admin
    waiting_msg_from_user = State()
    add_admin = State()

    # add channel
    channel_management = State()
    get_channel_data = State()
    get_channel_link = State()
    add_channel = State()
    choose_channel_for_delete = State()
    del_channel = State()

    # test state
    test = State()
