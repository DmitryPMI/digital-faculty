
import re
import datetime
import time 
import locale
from data import get_rasp_day, get_rasp
from lev_distance import lev_dist, req_distance

days = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота", 6: "Воскресение"}
today = days[time.localtime().tm_wday]
next_day = days[time.localtime().tm_wday + 1]
#print(today)

def get_date(words):

	for word in words:
		date = re.fullmatch("[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])", word)
		if date != None:
			return date
	pass

def show_rasp():

	print("Привет, чем могу быть полезен?")
	request = str(input())
	print("Какая группа?")
	group = str(input())

	words = request.split()
	date = get_date(words)

	if req_distance(words, "расписание"):

		if req_distance(words, "сегодня"):
			#print(get_rasp_day(group, today))
			return get_rasp_day(group, today)
		elif req_distance(words, "завтра"):
			#print(get_rasp_day(group, next_day))
			return get_rasp_day(group, next_day)
		elif date != None:
			then_date = datetime.date(int(time.localtime().tm_year), int(date.group(1)),  int(date.group(2)))
			day = days[then_date.weekday()]
			return get_rasp_day(group, day)

		return get_rasp(group)

	return "Не понял запрос :("



print(show_rasp())
#print(datetime.datetime.now())
#print(today, type(today), next_day)

#date = re.fullmatch("[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])", input())
#then_date = datetime.date(int(time.localtime().tm_year), int(date.group(1)),  int(date.group(2)))
#print(date)
#print(type(date, time.localtime().tm_year), date.group(1), date.group(2))
#print(days[then_date.weekday()])