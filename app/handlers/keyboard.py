from typing import List
from aiogram import types

def make_usual_keyboard(keys: List[str], columns: int):
    if len(keys) == 0:
        keyboard=types.ReplyKeyboardRemove()
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=columns, resize_keyboard=True)
        tg_keys = []
        for key in keys:
            tg_keys.append(types.KeyboardButton(text=key))
        keyboard.add(*tg_keys)
    return keyboard


def make_inline_keyboard(keys: List[str], columns: int):
    pass


def make_keyboard(keys: List[str], type: str="usual", columns: int=1):

    if type == "usual":
        keyboard = make_usual_keyboard(keys, columns)
    else:
        keyboard = make_inline_keyboard(keys, columns)
    return keyboard