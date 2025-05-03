from aiogram.types import(
    ReplyKeyboardMarkup,
    KeyboardButton
)

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ударения'),
            KeyboardButton(text='Трудные слова (9)')
        ],
        [
            KeyboardButton(text='Словарные слова'),
            KeyboardButton(text='Суффиксы глаголов')
        ],
        [
            KeyboardButton(text='Пре При')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

action_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать (рандом)'),
            KeyboardButton(text='Начать (отработка)')
        ],
        [
            KeyboardButton(text='Рекорд'),
            KeyboardButton(text='Топ ошибок')

        ],
        [
            KeyboardButton(text='Сбросить статистику'),
            KeyboardButton(text='Все слова')
        ],
        [
            KeyboardButton(text='Назад')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)