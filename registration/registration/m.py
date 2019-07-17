import sqlite3
from db_users import*
from data import*

conn = sqlite3.connect("database_rasp.db")
cursor = conn.cursor()

show_db('users')

def find_user_name(f_name,l_name):
	sql = "SELECT * FROM students WHERE first_name=:first_name AND last_name=:last_name"
	cursor.execute(sql,{"first_name": f_name,"last_name": l_name})
	return cursor.fetchall()
def group_in_base(table_name,group):
	sql = 'SELECT * FROM ' + table_name + ' WHERE name=?'
	cursor.execute(sql, [(group)])
	return len(cursor.fetchall()) != 0

def find_group_in_base(group):
	sql = 'SELECT * FROM groups WHERE name=?'
	cursor.execute(sql, [(group)])
	return cursor.fetchall()

def show_db_for_user(table_name):
	


def show_db(table_name):
	sql = 'SELECT * FROM ' + table_name + ' ORDER BY id'
	print("\nHere's a listing of all the records in the table " + table_name +":")
	for row in cursor.execute(sql):
		print(row)