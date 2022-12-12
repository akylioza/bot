from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from states.states import ApplicationFSMAdmin

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.dispatcher.filters.state import State, StatesGroup


from keyboards.client import client_keyboard

from bot import bot
from bot import dp

from db import sqlite_db


async def start_command(message: types.Message):
    await message.answer('Choose your next option', reply_markup=client_keyboard)


async def create_application(message: types.Message):
    await ApplicationFSMAdmin.name.set()
    await message.answer("type your name")

async def set_client_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await ApplicationFSMAdmin.next()
    await message.answer('опишите ваше состояние')

async def set_client_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await ApplicationFSMAdmin.next()
    await message.answer('какую дату вам бы хотелось?')

async def set_client_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await ApplicationFSMAdmin.next()
    await message.answer('какое время вам бы хотелось?')

async def set_client_time(message: types.Message, state: FSMContext):
    doctur = sqlite_db.cursor.execute('SELECT * FROM doctor').fetchall()
    async with state.proxy() as data:
        data['time'] = message.text
    await ApplicationFSMAdmin.next()
    await message.answer(f'к какому доктору вам бы хотелось?')
    for doc in doctur:
        await bot.send_message(message.from_user.id, f'name: {doc[1]}')

async def set_client_doctor(message: types.Message, state: FSMContext):
    applic_red = sqlite_db.cursor.execute("SELECT * FROM application ORDER BY application_id DESC LIMIT 1").fetchall()
    async with state.proxy() as data:
        data['doc'] = message.text
    await sqlite_db.sql_add_command(state, 'application')
    await state.finish()
    await message.answer('ваша заявка принята')
    for item in applic_red:
        await bot.send_message(message.from_user.id, f'name: {item[1]}\ndescription: {item[2]}\ndate: {item[3]}\ntime: {item[4]}')


def register_application_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(create_application, commands=['create_application'], state=None)
    dp.register_message_handler(set_client_name, state=ApplicationFSMAdmin.name)
    dp.register_message_handler(set_client_description, state=ApplicationFSMAdmin.description)
    dp.register_message_handler(set_client_date, state=ApplicationFSMAdmin.date)
    dp.register_message_handler(set_client_time, state=ApplicationFSMAdmin.time)
    dp.register_message_handler(set_client_doctor, state=ApplicationFSMAdmin.doc)
