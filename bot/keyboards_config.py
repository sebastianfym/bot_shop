from aiogram import types

kb_main_menu = [
        [types.KeyboardButton(text="Каталог")],
        [types.KeyboardButton(text="Корзина")],
        [types.KeyboardButton(text="FAQ")]
    ]

confirmation_buttons = [
    [types.KeyboardButton(text="Да")],
    [types.KeyboardButton(text="Нет")],
]

start_buttons = [
    [types.KeyboardButton(text="/start",)]
]

kb_main = types.ReplyKeyboardMarkup(keyboard=kb_main_menu, resize_keyboard=True, one_time_keyboard=True)

kb_confirmation = types.ReplyKeyboardMarkup(keyboard=confirmation_buttons, resize_keyboard=True, one_time_keyboard=True)

kb_start = types.ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True, one_time_keyboard=True)
