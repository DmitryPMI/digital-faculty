import re
import sqlite3
from datetime import datetime

# data base part

def get_group_list(user_id):
	global db
	row = db.execute("SELECT * FROM 'students' WHERE 'students'.'id' = ?;", (user_id, )).fetchone()

	if(row != None):
		group_id = row["group_id"]
		rows = db.execute("SELECT * FROM 'students' WHERE 'students'.'group_id' = ?;", (group_id, )).fetchall()

		if(rows != None):
			return rows
		else:
			print("Internal error: group with id = " + str(group_id) + " not found.")
	else:
		print("Internal error: user with id = " + str(user_id) + " not found.")

def get_not_mark_group_list(user_id):
	global db
	row = db.execute("SELECT * FROM 'students' WHERE 'students'.'id' = ?;", (user_id, )).fetchone()

	if(row != None):
		group_id = row["group_id"]
		rows = db.execute("SELECT * FROM 'students' WHERE 'students'.'group_id' = ? AND 'students'.'id' NOT IN (SELECT 'attendance'.'user_id' FROM 'attendance' WHERE 'attendance'.'date' = ?)", (group_id, date, )).fetchall()

		if(rows != None):
			return rows
		else:
			print("Internal error: group with id = " + str(group_id) + " not found.")
	else:
		print("Internal error: user with id = " + str(user_id) + " not found.")

def get_status_group(user_id):
	global db
	row = db.execute("SELECT * FROM 'students' WHERE 'students'.'id' = ?;", (user_id, )).fetchone()

	if(row != None):
		group_id = row["group_id"]
		rows = db.execute("SELECT 'students'.'name' AS 'students_name', 'status_attendance'.'name' as 'status_name' FROM 'attendance' INNER JOIN 'status_attendance' ON 'attendance'.'status' = 'status_attendance'.'id' INNER JOIN 'students' ON 'attendance'.'user_id' = 'students'.'id' WHERE 'students'.'group_id' = ?;", (group_id, )).fetchall()

		if(rows != None):
			return rows
		else:
			print("Internal error: group with id = " + str(group_id) + " not found.")
	else:
		print("Internal error: user with id = " + str(user_id) + " not found.")

# main logic part

def show_group_list(user_id):
	group = get_group_list(user_id)

	for i in range(len(group)):
		print(i + 1, group[i]["name"])

def show_status_group(user_id):
	group = get_status_group(user_id)

	for i in range(len(group)):
		print(i + 1, group[i]["students_name"], group[i]["status_name"])

def mark_attend(user_id):
	global db
	global date
	db.execute("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)", (user_id, date, 2))

def mark_absent(user_id):
	global db
	global date
	db.execute("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)", (user_id, date, 3))

def mark_sick(user_id):
	global db
	global date
	db.execute("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)", (user_id, date, 4))

def change_data_for_past_days():
	print("change_data_for_past_days")

def correct_date(date):
	return re.match("[0-3][1-9].[0-1][1-2]", date) != None

def get_truggers(period):
	print("get_truggers")

def get_truggers_statistic():
	print("get_truggers_statistic")

# acts
def act_mark_absent(captain_id):
	ls = list(map(lambda it: {"value": it["name"], "action": lambda: mark_absent(it["id"])}, get_not_mark_group_list(captain_id)))
	interface("Выберите отсутствующего:", ls)

def act_mark_attend(captain_id):
	ls = list(map(lambda it: {"value": it["name"], "action": lambda: mark_attend(it["id"])}, get_not_mark_group_list(captain_id)))
	interface("Выберите присутствующего:", ls)

def act_mark_sick(captain_id):
	ls = list(map(lambda it: {"value": it["name"], "action": lambda: mark_sick(it["id"])}, get_not_mark_group_list(captain_id)))
	interface("Выберите болеющего:", ls)

def act_change_data_for_past_days():
	print("Введите дату в формате: dd.mm")
	date = input()
	if(correct_date(date)):
		change_data_for_past_days(date)
	else:
		print("Некорректный формат")

# interface
def interface(message, keyboard):
	print(message)
	print("____________\n")
	for key in keyboard:
		print(key["value"])

	print()

	q = input()
	for key in keyboard:
		if(q == key["value"]):
			key["action"]()
			return True
	print("Неверный запрос")
	return False

# Data base including and initialization

db = sqlite3.connect('db.sqlite3', check_same_thread=False)
db.row_factory = sqlite3.Row
now = datetime.now()
date = str(now.day) + '.' + str(now.month) + '.' + str(now.year)

# Authorization imitation

def get_user(user_id):
	global db
	row = db.execute("SELECT * FROM 'students' WHERE 'students'.'id' = ?;", (user_id, )).fetchone()

	if(row != None):
		return row["name"]
	else:
		print("Internal error: user with id = " + str(user_id) + " not found!")


captain_id = 1
print("Привет, " + get_user(captain_id))

interface("Чем хотите заняться?", [
	{"value": "Посмотреть список группы", "action": lambda: show_group_list(captain_id)},
	{"value": "Посмотреть текущий статус группы", "action": lambda: show_status_group(captain_id)},
	{"value": "Отметить посещаемость", "action": lambda: interface("Кого хотите отметить?", [
		{"value": "Отсутствующих сегодня", "action": lambda: act_mark_absent(captain_id)},
		{"value": "Присутствующих сегодня", "action": lambda: act_mark_attend(captain_id)},
		{"value": "Болеющих сегодня", "action": lambda: act_mark_sick(captain_id)},
		#{"value": "Изменить данные за прошлые дни", "action": act_change_data_for_past_days}
	])},

	#{"value": "Получить статистику", "action": lambda: interface("Какая статистика вас интересует?", [
	#	{"value": "Студенты, пропустившие пары вчера", "action": lambda: print(get_truggers(1))},
	#	{"value": "Студенты, пропустившие пары за неделю", "action": lambda: print(get_truggers(7))},
	#	{"value": "Студенты, пропустившие пары за две недели", "action": lambda: print(get_truggers(14))},
	#	{"value": "Полная статистика по пропущенным занятиям", "action": lambda: print(get_truggers_statistic())}
	#])}
])

db.commit()
db.close()