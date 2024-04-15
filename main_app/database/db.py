import sqlite3

'''
Добавил на случай если расширять таблицу
'''
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
id INTEGER PRIMARY KEY,
login TEXT(127) NOT NULL,
password TEXT(255) NOT NULL
)
''')

connection.commit()
connection.close()