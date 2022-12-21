from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from parse import message_parse
from googlesheet_table import view_xlsx, get_range
from table import create_answer
import sqlite3 as sql
from kb import main_menu


bot = Bot(token='5773486947:AAF-MNZlIq7_y3Zlbu4tqbAKnj465mbVchA')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def sql_start():
    global base, cursor
    base = sql.connect('timetablechanges.db')
    cursor = base.cursor()
    if base:
        print('Date base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS changes(date TEXT,photo TEXT)')
    base.commit()


async def add_timetable_changes(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO changes VALUES (?, ?)', tuple(data.values()))
        base.commit()


sql_start()


@dp.message_handler(commands=['start', 'help'])
async def start_menu(message: types.Message):
    start_message: str = (
        f'Здравствуйте. Это телеграм бот 426 гимназии.\n'
        f'Он поможет узнать расписание уроков и последнии\n'
        f'изменения в школьном расписании.\n'
        f'   КОМАНДЫ ДЛЯ ЧАТ-БОТА:\n\n'
        f'/расписание - команда для просмотра расписания.\n'
        f'После ввода команды потребуется вручную слитно\n'
        f'ввести год обучения и букву класса.\n'
        f'/просмотреть_изменения - команда для просмотра\n'
        f'последних изменений в расписании.'
        f'/start или /help команды для просмотра описания'
        f'возможностей телеграм бота.'
    )
    await bot.send_message(message.from_user.id, start_message, reply_markup=main_menu)
    

@dp.message_handler(commands=['просмотреть_изменения'])
async def view_timetablechanges(message: types.Message):
    last_changes = cursor.execute('SELECT * FROM changes').fetchall()[-1]
    await bot.send_photo(message.from_user.id, last_changes[1], last_changes[0], reply_markup=main_menu)


class TimetableChanges(StatesGroup):
    date = State()
    photo = State()


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
    await message.answer(time_table, reply_markup=main_menu)
    await state.finish()


@dp.message_handler(commands=['добавитьизменения'])
async def create_timetable_changes(message: types.Message):
    await message.answer("Введите дату изменений.")
    await TimetableChanges.date.set()


@dp.message_handler(state=TimetableChanges.date)
async def get_timetable_changes_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Отправьте фотографию изменений.")
    await TimetableChanges.photo.set()


@dp.message_handler(content_types=['photo'], state=TimetableChanges.photo)
async def get_timetable_changes_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    await message.answer(f"Имя: {data['date']}\n"f"Адрес: {data['photo']}")
    await add_timetable_changes(state)
    await state.finish()


executor.start_polling(dp, skip_updates=True)