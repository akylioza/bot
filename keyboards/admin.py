from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)

bt1 = KeyboardButton('/create_doctor')
bt2 = KeyboardButton('/doc_list')
bt3 = KeyboardButton('/application_list')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(bt1).insert(bt2).insert(bt3)