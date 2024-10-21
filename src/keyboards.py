from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from utils.callback_templates import autodelete_timer_is_template
from utils.time import get_autodelete_time_from_str

delete_btn = InlineKeyboardButton('Удалить', callback_data='delete_photo')
delete_kb = InlineKeyboardMarkup().add(delete_btn)

remove = ReplyKeyboardRemove()

# Выбор времени для отложки
time_2 = InlineKeyboardButton('0, 15, 19', callback_data='0, 15, 19')
time_3 = InlineKeyboardButton('11, 16, 21 (Alight)', callback_data='11, 16, 21')
time_4 = InlineKeyboardButton('11, 15, 19, 23', callback_data='11, 15, 19, 23')
time_5 = InlineKeyboardButton('10, 13, 16, 19, 22', callback_data='10, 13, 16, 19, 22')
choose_time_kb = InlineKeyboardMarkup(row_width=1).add(time_2, time_3, time_4, time_5)

accept_btn = InlineKeyboardButton('Начать планирование', callback_data='accept')
finish_schedule_kb = InlineKeyboardMarkup().add(accept_btn)

done_btn = KeyboardButton('Готово')
done_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(done_btn)


# Yes or No buttons
class YesOrNo(InlineKeyboardMarkup):
    yes_btn = InlineKeyboardButton('Да', callback_data='yes')
    no_btn = InlineKeyboardButton('Нет', callback_data='no')

    def __init__(self):
        super().__init__()
        self.add(self.yes_btn, self.no_btn)


class DelAdmin(InlineKeyboardMarkup):
    button = InlineKeyboardButton('Удалить', callback_data='delete')

    def __init__(self):
        super().__init__()
        self.add(self.button)


def create_channel_buttons(channels: list[dict]):
    buttons = []
    for channel_info in channels:
        title = channel_info.get('title')
        _id = channel_info.get('id')

        channel = InlineKeyboardButton(text=title, callback_data=_id)
        buttons.append(channel)

    return buttons


class ChannelServiceButtons(InlineKeyboardMarkup):
    add_channel = InlineKeyboardButton('➕Добавить канал', callback_data='add_channel')
    del_channel = InlineKeyboardButton('🗑Удалить канал', callback_data='del_channel')
    cancel_button = InlineKeyboardButton('❌Отменить', callback_data='cancel')

    buttons = [add_channel, del_channel, cancel_button]

    def __init__(self):
        super().__init__()


class Channels(InlineKeyboardMarkup):

    buttons = None

    def __init__(self, channels: list[dict]):
        super().__init__()

        self.buttons = create_channel_buttons(channels)
        row = []
        for button in self.buttons:
            row.append(button)
            if len(row) == 2:
                self.row(*row)
                row = []
        if row:
            self.row(*row)

    def delete_channel(self, channel_id):
        if not self.buttons:
            return

        for button in self.buttons:
            if button.callback_data == channel_id:
                self.buttons.remove(button)

    def add_channel(self, title, channel_id):
        channel = InlineKeyboardButton(text=title, callback_data=channel_id)
        self.buttons.append(channel)


class ChannelsWithServiceButtons(Channels, ChannelServiceButtons):
    service_buttons = ChannelServiceButtons.buttons

    def __init__(self, channels: list[dict]):
        super().__init__(channels=channels)

        row = []
        for button in self.service_buttons:
            row.append(button)
            if len(row) == 2:
                self.row(*row)
                row = []
        if row:
            self.row(*row)
