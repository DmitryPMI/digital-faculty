import sqlite3

conn = sqlite3.connect("database_rasp.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name text, last_name text, group_id text)""") #БД университета
cursor.execute("""CREATE TABLE groups (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#БД групп
cursor.execute("""CREATE TABLE days (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
cursor.execute("""CREATE TABLE time (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")
cursor.execute("""CREATE TABLE subjects (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
cursor.execute("""CREATE TABLE audience (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
cursor.execute("""CREATE TABLE rasp (id_group INTEGER  NOT NULL, id_day INTEGER NOT NULL, id_time INTEGER NOT NULL, id_audience INTEGER  NOT NULL, id_subject INTEGER  NOT NULL)""")#
cursor.execute("""CREATE TABLE access_status (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, status text)""")#
cursor.execute("""CREATE TABLE attendance_status (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, status text)""")

cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, student_id integer, group_id integer, admin_acces integer)""") #пользователи бота

cursor.execute("""CREATE TABLE attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id integer, date text, visited INTEGER)""") #посещаемость

cursor.execute("INSERT INTO access_status (status) VALUES ('Не указано')")
cursor.execute("INSERT INTO access_status (status) VALUES ('Студент')")
cursor.execute("INSERT INTO access_status (status) VALUES ('Рассмотрение заявки на старосту')")
cursor.execute("INSERT INTO access_status (status) VALUES ('Староста')")
cursor.execute("INSERT INTO access_status (status) VALUES ('Рассмотрение заявки на работника деканата')")
cursor.execute("INSERT INTO access_status (status) VALUES ('Работник деканата')")

cursor.execute("INSERT INTO attendance_status (status) VALUES ('Не отмечено')")
cursor.execute("INSERT INTO attendance_status (status) VALUES ('Присутствовал')")
cursor.execute("INSERT INTO attendance_status (status) VALUES ('Отсутствовал')")
cursor.execute("INSERT INTO attendance_status (status) VALUES ('Болел')")

cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Олег', 'Дудник', '1')")
cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Дмитрий', 'Сафонов', '1')")
cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Софья', 'Карпова', '1')")
cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Даниил', 'Рашин', '3')")

cursor.execute("INSERT INTO groups (name) VALUES ('ПМ-1701')")
cursor.execute("INSERT INTO groups (name) VALUES ('ПМ-1601')")
cursor.execute("INSERT INTO groups (name) VALUES ('БИ-1801')")

conn.commit()




