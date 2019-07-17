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

	print("https://api.vk.com/method/" + method + "?v=5.52&access_token=" + access_token + args)
	return requests.get("https://api.vk.com/method/" + method + "?v=5.52&access_token=" + access_token + args)

@csrf_exempt
def index(request):

	global access_token

	try:
		j = json.loads(request.body.decode('utf-8'))
		print('ss')
		print(j)
		print('ss')
	except:
		pass

	if('type' in j and j['type'] == 'message_new' and 'group_id' in j and j['group_id'] == 173566145 and 'object' in j):
		query("messages.send", user_id=j['object']['user_id'], message=j['object']['body'][::-1])

	if('type' in j and 'group_id' in j):
		if(j['type'] == 'confirmation' and j['group_id'] == 173566145):
			return HttpResponse('7b220efd')

	return HttpResponse('Everything will be fine)')