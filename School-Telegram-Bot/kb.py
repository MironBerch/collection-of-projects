from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_timetable = KeyboardButton('/Расписание')
button_timetable_changes_view = KeyboardButton('/Просмотреть_изменения')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(button_timetable).add(button_timetable_changes_view)