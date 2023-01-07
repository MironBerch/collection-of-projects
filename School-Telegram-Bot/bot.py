from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3 as sql
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text


button_timetable = KeyboardButton('/Расписание')
button_timetable_changes_view = KeyboardButton('/Просмотреть_изменения')
function_break_button = KeyboardButton('/отмена')
break_menu = main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(button_timetable).add(button_timetable_changes_view)
break_menu.add(function_break_button)

async def create_answer(xlsx):
    subjects = xlsx[0]
    rooms = xlsx[-1]
    answer = ['Расписание:\n']
    days = ['\nПонедельник:\n', '\nВторник:\n', '\nСреда:\n', '\nЧетверг:\n', '\nПятница:\n', '\nСубота:\n',]
    day = 0
    start_day_index = [0, 7, 14, 21, 28, 35]
    for object in range(len(subjects)):
        if object in start_day_index:
            answer.append(days[day])
            day+=1
        answer.append(str(subjects[object]))
        answer.append(' - ')
        answer.append(str(rooms[object]))
        answer.append('\n')
    s = ''.join(answer)
    return s

YEAR = {'5': 'Лист5', '6': 'Лист6', '7': 'Лист7', '8': 'Лист8', '9': 'Лист9', '10': 'Лист10', '11': 'Лист11'}
CLASS = {'а': 'а', 'б': 'б', 'в': 'в'}

async def get_range(class_letter: str, year_study: str) -> str:
    page = YEAR[year_study]
    class_letter = CLASS[class_letter]
    if class_letter == 'а': columns = 'B2:C42'
    if class_letter == 'б': columns = 'D2:E42'
    if class_letter == 'в': columns = 'F2:G42'
    range_data = page + '!' + columns
    return range_data

async def view_xlsx(values_range: str):
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1e2NCxgEcnBlwuh6VhugKXk-swmtuXsKH3qu-g77wogA'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=values_range,
        majorDimension='COLUMNS'
    ).execute()
    values = values['values']
    return values

bot = Bot(token='5773486947:AAF-MNZlIq7_y3Zlbu4tqbAKnj465mbVchA')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def message_parse(data):
    year_study = data['scholl_class'][0:-1].lower()
    class_letter = data['scholl_class'][-1].lower()
    context = {
        'class_letter': class_letter,
        'year_study': year_study
    }
    return context

def sql_start():
    global base, cursor
    base = sql.connect('timetablechanges.db')
    cursor = base.cursor()
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
        f'Он поможет узнать расписание уроков и \n'
        f'последнии изменения в школьном расписании.\n'
        f'КОМАНДЫ ДЛЯ ЧАТ-БОТА:\n'
        f'  /расписание - команда для просмотра\n'
        f'расписания. После ввода команды потребуется\n'
        f'вручную слитно ввести год обучения и букву класса.\n'
        f'  /просмотреть_изменения - команда для\n'
        f'просмотра последних изменений в расписании.'
        f'  /start или /help команды для просмотра'
        f'описания возможностей телеграм бота.'
    )
    await bot.send_message(message.from_user.id, start_message, reply_markup=main_menu)

@dp.message_handler(commands=['просмотреть_изменения', 'changes'])
async def view_timetablechanges(message: types.Message):
    last_changes = cursor.execute('SELECT * FROM changes').fetchall()[-1]
    await bot.send_photo(message.from_user.id, last_changes[1], last_changes[0], reply_markup=main_menu)


class TimetableChanges(StatesGroup):
    date = State()
    photo = State()


class Timetable(StatesGroup):
    scholl_class = State()


@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None: await state.finish()
    await message.answer("Ок", reply_markup=main_menu)

@dp.message_handler(commands=['расписание', 'timetable'])
async def start_timetable_search(message: types.Message):
    await message.answer("Теперь введите класс.", reply_markup=break_menu)
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
    await message.answer("Введите дату изменений.", reply_markup=break_menu)
    await TimetableChanges.date.set()

@dp.message_handler(state=TimetableChanges.date)
async def get_timetable_changes_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Отправьте фотографию изменений.", reply_markup=break_menu)
    await TimetableChanges.photo.set()

@dp.message_handler(content_types=['photo'], state=TimetableChanges.photo)
async def get_timetable_changes_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    await message.answer(f"Имя: {data['date']}\n"f"Адрес: {data['photo']}")
    await add_timetable_changes(state)
    await state.finish()

executor.start_polling(dp, skip_updates=True)