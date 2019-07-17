from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

access_token = "555646e656438607b12a1a38608915c7bf764b2215c8f40c2f9ba670e0a643f472839b42653a630f9a10a"

def query(method, **kwargs):
	global access_token

	args = ""
	for key, value in kwargs.items():
		args += "&" + str(key) + "=" + str(value)

	#print("https://api.vk.com/method/" + method + "?v=5.52&access_token=" + access_token + args)
	return requests.get("https://api.vk.com/method/" + method + "?v=5.52&access_token=" + access_token + args)

@csrf_exempt
def index(request):

	global access_token

	try:
		j = json.loads(request.body.decode('utf-8'))
	except:
		return HttpResponse('Something bad :(')
	
	print('ss')
	print(j)
	print('ss')

	if('type' in j and j['type'] == 'message_new' and 'group_id' in j and j['group_id'] == 173566145 and 'object' in j):
		user_id = j['object']['user_id']
		message = logic(user_id, j['object']['body'])
		query("messages.send", user_id=user_id, message=message)

	if('type' in j and 'group_id' in j):
		if(j['type'] == 'confirmation' and j['group_id'] == 173566145):
			return HttpResponse('7b220efd')

	return HttpResponse('ok')


################ Logic
#### Убрать в отдельный файл!

def logic(user_id, message):

	answer = "Я вас не понял :("


	print(message)
	if(message == "Привет"):
		user = get_user_name(user_id)
		print(user)
		if(user != None):
			answer = 'Привет, ' + user['first_name']


	return answer

################ API
#### Убрать в отдельный файл!

def get_user_name(user_id):
	try:
		q = query("users.get", user_ids=user_id)
		print(q.json())
		j = q.json()
		print('kek')
	except:
		return None

	print('j')
	print(j)
	print('j')

	if('response' in j):
		response = j['response']
		print('response')
		print(response)
		print('response')
		if(len(response) > 0):
			return response[0]

	return None