from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать заказ'),KeyboardButton(text='Посмотреть мои заказы')],
    [KeyboardButton(text='Админ-панель')]
], resize_keyboard=True)