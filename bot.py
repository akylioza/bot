from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

storage = MemoryStorage()


bot = Bot(token="5456127749:AAHHIu1lma0huhhB9HXHt7NLM9rO5We0u0Y")
dp = Dispatcher(bot, storage=storage)
