from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
import config
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from parse import message_parse
from googlesheet_table import view_xlsx, get_range
from table import create_answer


bot = Bot(token=config.settings["TOKEN"])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Timetable(StatesGroup):
    scholl_class = State()
    

@dp.message_handler(commands=['расписание'])
async def start_timetable_search(message: types.Message):
    await message.answer("Теперь введите класс.")
    await Timetable.scholl_class.set()


@dp.message_handler(state=Timetable.scholl_class)
async def get_scholl_class(message: types.Message, state: FSMContext):
    await state.update_data(scholl_class=message.text)
    data = await message_parse(data = await state.get_data())
    values_range = await get_range(class_letter=data['class_letter'], year_study=data['year_study'])
    xlsx = await view_xlsx(values_range=values_range)
    time_table = await create_answer(xlsx)
    await message.answer(time_table)
    await state.finish()


executor.start_polling(dp, skip_updates=True)