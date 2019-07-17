import sqlite3

conn = sqlite3.connect("database_rasp.db")
cursor = conn.cursor()

#cursor.execute("""CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name text, last_name text, group_id text)""") #БД университета
#cursor.execute("""CREATE TABLE groups (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#БД групп
#cursor.execute("""CREATE TABLE days (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
#cursor.execute("""CREATE TABLE time (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")
#cursor.execute("""CREATE TABLE subjects (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
#cursor.execute("""CREATE TABLE audience (name text, id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)""")#
#cursor.execute("""CREATE TABLE access_status (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, status text)""")#
#cursor.execute("""CREATE TABLE attendance_status (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, status text)""")

#cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, student_id integer, group_id integer, admin_acces integer)""") #пользователи бота

#cursor.execute("""CREATE TABLE attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id integer, date text, visited INTEGER)""") #посещаемость

#cursor.execute("INSERT INTO access_status (status) VALUES ('Студент')")
#cursor.execute("INSERT INTO access_status (status) VALUES ('Рассмотрение заявки на старосту')")
#cursor.execute("INSERT INTO access_status (status) VALUES ('Староста')")
#cursor.execute("INSERT INTO access_status (status) VALUES ('Рассмотрение заявки на работника деканата')")
#cursor.execute("INSERT INTO access_status (status) VALUES ('Работник деканата')")

#cursor.execute("INSERT INTO attendance_status (status) VALUES ('Не отмечено')")
#cursor.execute("INSERT INTO attendance_status (status) VALUES ('Присутствовал')")
#cursor.execute("INSERT INTO attendance_status (status) VALUES ('Отсутствовал')")
#cursor.execute("INSERT INTO attendance_status (status) VALUES ('Болел')")

#cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Дмитрий', 'Сафонов', '1')")
#cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Софья', 'Карпова', '1')")
#cursor.execute("INSERT INTO students (first_name, last_name, group_id) VALUES ('Даниил', 'Рашин', '3')")

#cursor.execute("INSERT INTO groups (name) VALUES ('ПМ-1701')")
#cursor.execute("INSERT INTO groups (name) VALUES ('ПМ-1601')")
#cursor.execute("INSERT INTO groups (name) VALUES ('БИ-1801')")

#conn.commit()


def select_by_id(table_name, column_name, some_id):

	sql = "SELECT "+column_name+" FROM "+table_name+ " WHERE id=:id"
	cursor.execute(sql, {"id": some_id})
	return cursor.fetchone()[0]

def select_id_by_name(table_name, name):

	sql = "SELECT id FROM "+table_name+" WHERE name=:name"
	cursor.execute(sql, {"name": name})
	return cursor.fetchone()[0]

def get_id_from_table(table_name, value):

	sql = "SELECT id FROM " + table_name + " WHERE name=:name"
	cursor.execute(sql, {"name": value, "table_name": table_name})
	respone = cursor.fetchone()
	return -1 if(respone == None) else respone[0]

def get_rasp_day(group, day):

	group_id = get_id_from_table('groups', group)
	if(group_id == -1):
		print("Не найдена группа")
		pass

	day_id = get_id_from_table('days', day)
	if(day_id == -1):
		print("День не найден")
		pass

	sql = "SELECT * FROM rasp WHERE id_group=:id_group  AND id_day=:id_day"
	cursor.execute(sql, {"id_group": group_id,"id_day": day_id})
	rasp = cursor.fetchall()

	out = []

	for i in range(len(rasp)):

		time_id = rasp[i][2]
		audience_id = rasp[i][3]
		subject_id = rasp[i][4]

		time = select_by_id("time", "name", time_id)
		audience = select_by_id("audience", "name", audience_id)
		subject = select_by_id("subjects", "name", subject_id)

		out.append([time, audience, subject])
	respone = ""

	for i in out:
		for j in i:
			respone = respone + j + " "
		respone = respone + "\n"
	
	return respone

def get_rasp(group):

	group_id = get_id_from_table('groups', group)
	if(group_id == -1):
		print("Не найдена группа")
		pass

	sql = "SELECT * FROM rasp WHERE id_group=:id_group"
	cursor.execute(sql, {"id_group": group_id})
	rasp = cursor.fetchall()

	out = []

	for i in range(len(rasp)):

		day_id = rasp[i][1]
		time_id = rasp[i][2]
		audience_id = rasp[i][3]
		subject_id = rasp[i][4]

		day = select_by_id("days", "name", day_id)
		time = select_by_id("time", "name", time_id)
		audience = select_by_id("audience", "name", audience_id)
		subject = select_by_id("subjects", "name", subject_id)

		out.append([day, time, audience, subject])

	respone = ""

	for i in out:
		for j in i:
			respone = respone + j + " "
		respone = respone + "\n"
	return respone


def insert_sth_smw(table_name, value):
	sql = "INSERT INTO "+table_name+" (name) VALUES (?)"
	cursor.execute(sql, [(value)])
	conn.commit()


def insert_rasp(group, day, time, audience, subject):

	group_id = select_id_by_name("groups", group)
	day_id = select_id_by_name("days", day)
	time_id = select_id_by_name("time", time)
	audience_id = select_id_by_name("audience", audience)
	subject_id = select_id_by_name("subjects", subject)

	sql = """INSERT INTO rasp VALUES (?,?,?,?,?)"""
	cursor.executemany(sql, [(group_id, day_id, time_id, audience_id, subject_id)])
	conn.commit()

def select_days():
	cursor.execute("SELECT name FROM days")
	days = cursor.fetchall()

	return list(map(lambda x: x[0], days))

def select_groups():
	cursor.execute("SELECT name FROM groups")
	groups = cursor.fetchall()

	return list(map(lambda x: x[0], groups))


def group_in_base(table_name,group):
	sql = 'SELECT * FROM ' + table_name + ' WHERE name=?'
	cursor.execute(sql, [(group)])
	return len(cursor.fetchall()) != 0

def show_db(table_name):
	sql = 'SELECT * FROM ' + table_name + ' ORDER BY id'
	print("\nHere's a listing of all the records in the table " + table_name +":")
	for row in cursor.execute(sql):
		print(row)

def username_in_base(first_name, last_name):
	if len(find_user_name(first_name,last_name)) != 0:
		return True
	else:
		return False

def delete_user(table_name, name):
	sql = 'DELETE FROM ' + table_name + ' WHERE name = \'' + name + '\''
	cursor.execute(sql)
	conn.commit()

def find_group_in_base(group):
	sql = 'SELECT * FROM groups WHERE name=?'
	cursor.execute(sql, [(group)])
	return cursor.fetchall()

def find_user_id(db,table_name, u_id):
	sql = 'SELECT * FROM ' + table_name + ' WHERE id=?'
	cursor.execute(sql, [(u_id)])
	return cursor.fetchall()

def add_new_user(student_id, group_id, adm_acc):
	sql = 'INSERT INTO users (student_id, group_id, admin_acces) VALUES (?,?,?)'
	cursor.execute(sql, (student_id, group_id, adm_acc))
	conn.commit()

def add_new_user(db,table_name, u_id, name, gr, adm_acc):
	if user_in_base(db,table_name,u_id):
		print('You are already in base')
	else:
		sql = 'INSERT INTO ' + table_name + ' VALUES (\'' + u_id +'\', \'' + name +'\', \'' + gr +'\', \'' + adm_acc + '\')'
		conn = sqlite3.connect(db)
		cursor = conn.cursor()
		cursor.execute(sql)
		conn.commit()

def find_user_name(f_name,l_name):
	sql = "SELECT * FROM students WHERE first_name=:first_name AND last_name=:last_name"
	cursor.execute(sql,{"first_name": f_name,"last_name": l_name})
	return cursor.fetchall()

insert_sth_smw("groups", "ПМ-1701")
insert_sth_smw("groups", "ПМ-1802")
insert_sth_smw("subjects", "Алгебра")
insert_sth_smw("subjects", "Философия")
insert_sth_smw("subjects", "Социология")
insert_sth_smw("subjects", "Диффуры")
insert_sth_smw("audience", "2015")
insert_sth_smw("audience", "3012")
insert_sth_smw("time", "9:00")
insert_sth_smw("time", "10:50")
insert_sth_smw("days", "Понедельник")
insert_sth_smw("days", "Вторник")
insert_sth_smw("days", "Среда")
insert_sth_smw("days", "Четверг")
insert_sth_smw("days", "Пятница")
insert_sth_smw("days", "Суббота")
insert_rasp("ПМ-1701", "Среда", "9:00", "2015", "Алгебра")
insert_rasp("ПМ-1701", "Среда", "10:50", "3012", "Философия")

insert_rasp("ПМ-1802", "Четверг", "9:00", "2015", "Социология")
insert_rasp("ПМ-1802", "Четверг", "10:50", "3012", "Диффуры")

insert_rasp("ПМ-1802", "Пятница", "9:00", "2015", "Философия")
insert_rasp("ПМ-1802", "Пятница", "10:50", "3012", "Алгебра")



