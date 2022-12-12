from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ApplicationFSMAdmin(StatesGroup):
    name = State()
    description = State()
    date = State()
    time = State()
    doc = State()

class DoctorFSMAdmin(StatesGroup):
    name = State()
    photo = State()