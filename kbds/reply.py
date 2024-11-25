from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(*btns: str, sizes: tuple[int] = (2,), placeholder: str = None):

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns):
        keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder,
    )
