import sqlite3


def sql_start():
    global base, cursor
    base = sqlite3.connect('db.sqlite3')
    cursor = base.cursor()
    if base:
        print('Database connected')

        base.execute(
            'CREATE TABLE IF NOT EXISTS doctor(doctor_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, photo TEXT)'
        )
        base.execute(
            'CREATE TABLE IF NOT EXISTS application(application_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, description TEXT, date TEXT, time TEXT, doc TEXT, FOREIGN KEY(doc) REFERENCES doctor(name))'
        )
        base.commit()



async def sql_add_command(state, table):

    if table == 'doctor':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?)'
        
    elif table == 'application':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?)'

    async with state.proxy() as data:
        cursor.execute(
            insert_query, (None, *data.values())
        )

        base.commit()