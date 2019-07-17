########### Подключение к бд ###########
########### Исправить!

from db_users import *

db = 'database_rasp.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()

answer = 0
group = ''


###########

#print('Я - деканат-бот - приветствую вас!')

while answer == 0:
	inp = input('вход или регистрация? ').lower()# скорее всего будут кнопочки, поэтому обработку ошибок делать не надо
	if inp.lower() == 'регистрация':
#		u_id = input('введите ваш id: ') #потом не вводим вход через учётную запись VK или Telegram
		first_name = input('введите ваше имя: ')
		last_name = input('введите вашу фамилию: ')
		user = find_user_name(first_name, last_name)
		if len(user) == 0:
			print('такого пользователя нет! Попробуйте найти ошибку или пройдите регистрацию!')
			continue
		else:
#
			id_user = user[0][0]
			status = input('Вы студент? (да\нет): ').lower()
			if status == 'да':
				m_status = input('Вы староста? (да\нет): ').lower()
				if m_status == 'да':
					adm_acc = '3'
					print('Отправлена заявка на подтверждения вашего статуса старосты.')
				else:
					adm_acc = '2'

				while group == '':
					group = input('введите вашу группу: ').upper()
					gr = find_group_in_base(group)
					if len(gr) != 0:
						id_group = gr[0][-1]
						add_new_user(id_user, id_group, adm_acc)
					else:
						print('Такой группы не существует! Повторите ввод')
						group = ''
				answer = 1
#
			else:
				status = input('вы сотрудник деканата? (да\нет): ').lower()
				if status == 'да':
					adm_acc = '5'
					group = 0
					id_group = 0
					add_new_user(id_user, id_group, adm_acc)
					print('Отправлена заявка на подтверждения вашего статуса сотрудника деканата.')
					answer = 1
				else:
					print('Была допущена ошибка. Начните сначала.')

	else:
#		u_id = input('введите ваш id: ') #потом не вводим
		name = input('введите ваше имя: ')
		if user_in_base(table_name, name):
			print('Вход выполнен')#Вход
			answer = 1


conn.commit()

show_db("users")