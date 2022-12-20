import sqlite3 as sql


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


#async def read_timetable_changes(message):
    #for obj in cursor.execute('SELECT * FROM changes').fetchall():
        #pprint(obj, obj[0], obj[1], '\n')
        #await bot.send_photo(message.from_user.id, obj[0], obj[1])

    #ls = cursor.execute('SELECT * FROM changes').fetchall()
    #print(ls[-1])