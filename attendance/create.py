import sqlite3

db = sqlite3.connect('db.sqlite3', check_same_thread=False)
db.row_factory = sqlite3.Row

db.execute('''CREATE TABLE groups (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name text)''')
db.execute("INSERT INTO groups (id, name) VALUES (1, 'ПМ-1701')")
db.execute("INSERT INTO groups (id, name) VALUES (2, 'ИБ-1801')")

db.execute('''CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name text, group_id integer)''')
db.execute("INSERT INTO students (name, group_id) VALUES ('Дудник Олег', 1)")
db.execute("INSERT INTO students (name, group_id) VALUES ('Сафонов Дмитрий', 1)")
db.execute("INSERT INTO students (name, group_id) VALUES ('Карпова Софья', 1)")
db.execute("INSERT INTO students (name, group_id) VALUES ('Даниил Рашин', 2)")

db.execute('''CREATE TABLE attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id integer, date text, status INTEGER)''')

db.execute('''CREATE TABLE status_attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name text)''')
db.execute("INSERT INTO status_attendance (id, name) VALUES (1, 'Не отмечено')")
db.execute("INSERT INTO status_attendance (id, name) VALUES (2, 'Присутствовал')")
db.execute("INSERT INTO status_attendance (id, name) VALUES (3, 'Отсутствовал')")
db.execute("INSERT INTO status_attendance (id, name) VALUES (4, 'Болеет')")

db.commit()
db.close()