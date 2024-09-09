from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def get_callback_btns(
    *,
    butns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in butns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
