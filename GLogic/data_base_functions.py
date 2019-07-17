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

def delete_user(table_name, name):
	sql = 'DELETE FROM ' + table_name + ' WHERE name = \'' + name + '\''
	cursor.execute(sql)
	conn.commit()

def delete_user(db, table_name, id):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	sql = 'DELETE FROM ' + table_name + ' WHERE id = \'' + id + '\''
	cursor.execute(sql)
	conn.commit()

def find_group_in_base(group):
	sql = 'SELECT * FROM groups WHERE name=?'
	cursor.execute(sql, [(group)])
	return cursor.fetchall()

def find_user_id(db,table_name, u_id):
	sql = 'SELECT * FROM ' + table_name + ' WHERE id=?'
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute(sql, [(u_id)])
	return cursor.fetchall()

def find_user_name(f_name,l_name):
	sql = "SELECT * FROM students WHERE first_name=:first_name AND last_name=:last_name"
	cursor.execute(sql,{"first_name": f_name,"last_name": l_name})
	return cursor.fetchall()

def get_id_from_table(table_name, value):
	sql = "SELECT id FROM " + table_name + " WHERE name=:name"
	cursor.execute(sql, {"name": value, "table_name": table_name})
	respone = cursor.fetchone()
	return -1 if(respone == None) else respone[0]


def get_rasp(group):

	group_id = get_id_from_table('groups', group)
	if(group_id == -1):
		print("Не найдена группа")
		return []

	sql = "SELECT * FROM rasp WHERE id_group=:id_group"
	cursor.execute(sql, {"id_group": group_id})
	rasp = cursor.fetchall()

	out = []

	for i in range(len(rasp)):

		day_id = rasp[i][1]
		time_id = rasp[i][2]
		audience_id = rasp[i][3]
		subject_id = rasp[i][4]

		sql = "SELECT name FROM days WHERE id=:id"
		cursor.execute(sql, {"id": day_id})
		day = cursor.fetchone()[0]

		sql = "SELECT name FROM time WHERE id=:id"
		cursor.execute(sql, {"id": time_id})
		time = cursor.fetchone()[0]

		sql = "SELECT name FROM audience WHERE id=:id"
		cursor.execute(sql, {"id": audience_id})
		audience = cursor.fetchone()[0]

		sql = "SELECT name FROM subjects WHERE id=:id"
		cursor.execute(sql, {"id": subject_id})
		subject = cursor.fetchone()[0]

		out.append([day, time, audience, subject])

	return out

def get_rasp_day(group, day):
	group_id = get_id_from_table('groups', group)
	if(group_id == -1):
		print("Не найдена группа")
		return []

	day_id = get_id_from_table('days', day)
	if(day_id == -1):
		print("День не найден")
		return []

	sql = "SELECT * FROM rasp WHERE id_group=:id_group  AND id_day=:id_day"
	cursor.execute(sql, {"id_group": group_id,"id_day": day_id})
	rasp = cursor.fetchall()

	out = []

	for i in range(len(rasp)):

		time_id = rasp[i][2]
		audience_id = rasp[i][3]
		subject_id = rasp[i][4]

		sql = "SELECT name FROM time WHERE id=:id"
		cursor.execute(sql, {"id": time_id})
		time = cursor.fetchone()[0]

		sql = "SELECT name FROM audience WHERE id=:id"
		cursor.execute(sql, {"id": audience_id})
		audience = cursor.fetchone()[0]

		sql = "SELECT name FROM subjects WHERE id=:id"
		cursor.execute(sql, {"id": subject_id})
		subject = cursor.fetchone()[0]

		out.append([time, audience, subject])

	return out

def group_in_base(table_name,group):
	sql = 'SELECT * FROM ' + table_name + ' WHERE name=?'
	cursor.execute(sql, [(group)])
	return len(cursor.fetchall()) != 0

def group_in_base(db,table_name,group):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	sql = 'SELECT * FROM ' + table_name + ' WHERE name=?'
	cursor.execute(sql, [(group)])
	if len(cursor.fetchall()) == 0:
		return False
	else:
		return True


def insert_group(group):

	sql = """INSERT INTO groups (name) VALUES (?)"""
	cursor.execute(sql, [(group)])
	conn.commit()

def insert_day(day):

	sql = """INSERT INTO days (name) VALUES (?)"""
	cursor.execute(sql, [(day)])
	conn.commit()

def insert_time(time):

	sql = """INSERT INTO time (name) VALUES (?)"""
	cursor.execute(sql, [(time)])
	conn.commit()

def insert_subject(subject):

	sql = """INSERT INTO subjects (name) VALUES (?)"""
	cursor.execute(sql, [(subject)])
	conn.commit()

def insert_audience(audience):

	sql = """INSERT INTO audience (name) VALUES (?)"""
	cursor.execute(sql, [(audience)])
	conn.commit()

def insert_rasp(group, day, time, audience, subject):

	sql = """SELECT id FROM groups WHERE name=:name"""
	cursor.execute(sql, {"name": group})
	group_id = cursor.fetchone()[0]

	sql = """SELECT id FROM days WHERE name=:name"""
	cursor.execute(sql, {"name": day})
	day_id = cursor.fetchone()[0]

	sql = """SELECT id FROM time WHERE name=:name"""
	cursor.execute(sql, {"name": time})
	time_id = cursor.fetchone()[0]

	sql = """SELECT id FROM audience WHERE name=:name"""
	cursor.execute(sql, {"name": audience})
	audience_id = cursor.fetchone()[0]

	sql = """SELECT id FROM subjects WHERE name=:name"""
	cursor.execute(sql, {"name": subject})
	subject_id = cursor.fetchone()[0]

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

def show_db(table_name):
	sql = 'SELECT * FROM ' + table_name + ' ORDER BY id'
	print("\nHere's a listing of all the records in the table " + table_name +":")
	for row in cursor.execute(sql):
		print(row)

def show_db(db,table_name):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	sql = 'SELECT * FROM ' + table_name + ' ORDER BY id'
	print("Here's a listing of all the records in the table:")
	for row in cursor.execute(sql):
		print(row)

def username_in_base(first_name, last_name):
	if len(find_user_name(first_name,last_name)) != 0:
		return True
	else:
		return False

def user_in_base(db,table_name, u_id):
	if len(find_user_id(db,table_name,u_id)) > 0:
		return True
	else:
		return False