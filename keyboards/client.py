from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)

bt1 = KeyboardButton('/create_application')

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
client_keyboard.add(bt1)