from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from states.states import ApplicationFSMAdmin, DoctorFSMAdmin

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)


from keyboards.admin import admin_keyboard

from bot import bot
from bot import dp

from db import sqlite_db

ID = None


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, "choose action: ", reply_markup=admin_keyboard
    )
    await message.delete()


async def create_doctor(message: types.Message):
    if message.from_user.id == ID:
        await DoctorFSMAdmin.name.set()
        await message.answer("type doctor's name")
    await message.answer("you'r not an admin")


async def set_doctor_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:    
        async with state.proxy() as data:
            data['name'] = message.text
        await DoctorFSMAdmin.next()
        await message.answer('пришлите фото')
    

async def set_doctor_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await sqlite_db.sql_add_command(state, table='doctor')
        await state.finish()
        await message.answer('Готово')




async def doctor_list(message: types.Message):
    for obj in sqlite_db.cursor.execute('SELECT * FROM doctor').fetchall():
        await bot.send_photo(
            message.from_user.id, obj[2],f'ID доктора: {obj[0]}\nимя доктора: {obj[1]}\n',)
                


async def apllication_list(message: types.Message):
    for item in sqlite_db.cursor.execute('SELECT * FROM application').fetchall():
        await bot.send_message(message.from_user.id, f'name: {item[1]}\ndescription: {item[2]}\ndate: {item[3]}\ntime: {item[4]}')



def register_doctor_handler(dp: Dispatcher):
    dp.register_message_handler(create_doctor, commands=['create_doctor'], state=None)
    dp.register_message_handler(set_doctor_name, state=DoctorFSMAdmin.name)
    dp.register_message_handler(set_doctor_photo, content_types=['photo'], state=DoctorFSMAdmin.photo)
    dp.register_message_handler(make_changes_command, commands=['admin'])
    dp.register_message_handler(doctor_list, commands=['doc_list'])
    dp.register_message_handler(apllication_list, commands=['application_list'])