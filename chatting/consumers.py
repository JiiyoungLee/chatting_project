from django.http import HttpResponse
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import ChattingRoom, UserLogin, UserMessage
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core import serializers
from collections import OrderedDict
from .forms import UserMessageForm
import json


@channel_session
def ws_message(message):
	Group("chat-%s" % message.channel_session['room']).send({
		"text": message.content['text'],
	})

@channel_session
@channel_session_user_from_http
def ws_add(message):
	room_number = message.content['query_string'].split('=')[1]
	message.channel_session['room'] = room_number
	Group("chat-%s" % room_number).add(message.reply_channel)
	message.reply_channel.send({
		"accept": True
	})

@channel_session
@channel_session_user
def ws_disconnect(message):
	Group("chat-%s" % message.channel_session['room']).send({
		"text": '{"sender": "<strong>SYSTEM</strong>", "msg": "<strong>'+message.user.username+' exits.</strong>"}',
		})
	this_user = User.objects.get(username=message.user.username)
	this_room = ChattingRoom.objects.get(id=message.channel_session['room'])
	this_room.member.remove(this_user)
	this_room.save()
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

@channel_session_user_from_http
def room_connect(message):
	#print("room_connect")
	Group("room").add(message.reply_channel)
	for room in ChattingRoom.objects.all():
		room_info = {'id': room.id, 'name': room.room_name, 
		'creator': room.creator, 
		'created_time': room.created_time.strftime("%Y-%m-%d"), 
		'member': room.member.all().count(), 
		'member_count': room.member_count
		}
		Group("room").send({
			"text": json.dumps(room_info) 
		})
	for user in UserLogin.objects.all():
		user_info = {'msg_code': 'info', 'id': user.user.id, 
		'username': user.user.username, 'is_loggedin': user.is_loggedin}
		Group("room").send({
			"text": json.dumps(user_info)
		})

	message.reply_channel.send({
		"accept": True,
	})
	"""
	Group("room").add(message.reply_channel)
	Group("room").send({
		"text": '{"user": "'+ message.user.username +'", "room": "connects", "from": "room_list"}',
	})
	message.reply_channel.send({
		"accept": True,
	})
	"""

@channel_session_user
def room_disconnect(message):
	#print("room_disconnect")
	Group("room").add(message.reply_channel)
	for room in ChattingRoom.objects.all():
		room_info = {'id': room.id, 'name': room.room_name, 
		'creator': room.creator, 
		'created_time': room.created_time.strftime("%Y-%m-%d"), 
		'member': room.member.all().count(), 
		'member_count': room.member_count
		}
		 
		Group("room").send({
			"text": json.dumps(room_info) 
		})

	for user in UserLogin.objects.all():
		user_info = {'msg_code': 'info', 'id': user.user.id, 
		'username': user.user.username, 'is_loggedin': user.is_loggedin}
		Group("room").send({
			"text": json.dumps(user_info)
		})
			
	Group("room").discard(message.reply_channel)
	"""Group("room").send({
		"text": '{"user": "'+ message.user.username +'", "room": "disconnects", "from": "room"}',
	})"""
	


def room_message(message):
	#print(message.content['text'])
	Group("room").send({
		"text": message.content['text'],
	})
	

def room_list_connect(message):
	#print("room_list_connect")
	Group("room").add(message.reply_channel)
	for room in ChattingRoom.objects.all():
		room_info = {'id': room.id, 'name': room.room_name, 
		'creator': room.creator, 
		'created_time': room.created_time.strftime("%Y-%m-%d"), 
		'member': room.member.all().count(), 
		'member_count': room.member_count
		}
		 
		Group("room").send({
			"text": json.dumps(room_info) 
		})

	for user in UserLogin.objects.all():
		user_info = {'msg_code': 'info', 'id': user.user.id, 
		'username': user.user.username, 'is_loggedin': user.is_loggedin}
		Group("room").send({
			"text": json.dumps(user_info)
		})
	
	message.reply_channel.send({
		"accept": True,
	})

def room_list_disconnect(message):
	#print("room_list_disconnect")
	Group("room").discard(message.reply_channel)

@channel_session	
def test_connect(message):
	Group("test").add(message.reply_channel)
	message.reply_channel.send({
		"accept": True
		})
	

@channel_session
def test_disconnect(message):
	Group("test").discard(message.reply_channel)

@channel_session
@channel_session_user_from_http
def test_message(message):
	print(message.content['text'])
	print(json.loads(message.content['text']))
	input_message = json.loads(message.content['text'])
	if input_message['code'] == 'msg' and 'receiver' in input_message:
		receiver = User.objects.get(username=input_message['receiver'])
		sender = User.objects.get(id=input_message['sender'])
		user_message = UserMessage(receiver=receiver, sender=sender, context=input_message['context'])
		user_message.save()
	if input_message['context'] == 'exit room':
		print("EXIT")
		room_id = input_message['room']
		this_room = ChattingRoom.objects.get(id=room_id)
		this_member = User.objects.get(username=input_message['sender'])
		this_room.member.remove(this_member)
		this_room.save()
	if input_message['context'] == 'logout':
		print("LOGOUT")
		this_user = User.objects.get(username=input_message['sender'])
		user_instance = UserLogin.objects.get(user=this_user)
		user_instance.is_loggedin = 0
		user_instance.save()
		these_rooms = ChattingRoom.objects.filter(member=this_user)
		for this_room in these_rooms:
			this_room.member.remove(this_user)
			this_room.save()
	if input_message['code'] == 'noti' and 'messageId' in input_message:
		this_message = UserMessage.objects.get(id=input_message['messageId'])
		this_message.is_checked = 1
		this_message.save()
	
	#message_dict = json.loads(message.content['text'])
	#print(message_dict)
	for room in ChattingRoom.objects.all():
		if room.member.all().count() == 0:
			room_info = json.dumps({'id': room.id,
				'delete': True
				})
			room.delete()
		else :
			room_info = json.dumps({'id': room.id, 
			'name': room.room_name, 
			'creator': room.creator, 
			'created_time': room.created_time.strftime("%Y-%m-%d"), 
			'member': room.member.all().count(), 
			'member_count': room.member_count,
			})
		Group("test").send({
			"text": json.dumps({'code': 'info room', 'sender': 'system', 'context': room_info})
			})
	for user in UserLogin.objects.all():
		join_room = []
		for join_rel in user.user.join.all():
			join_room.append(json.dumps({'room_id': join_rel.id, 'room_name': join_rel.room_name}))
		user_info = json.dumps({'id': user.user.id, 
		'username': user.user.username,
		'is_loggedin': user.is_loggedin,
		'join_member': join_room
		})
		Group("test").send({
			"text": json.dumps({'code': 'info user', 'sender': 'system', 'context': user_info})
			})
	Group("test").send({
		"text": message.content['text'],
		})

	for slip_message in UserMessage.objects.filter(is_checked=0):
		print(slip_message)	
		slip_message_info = json.dumps({'id':slip_message.id, 
		'sender': slip_message.sender.username,
		'receiver': slip_message.receiver.username,
		'context': slip_message.context,
		'send_time': slip_message.created_time.strftime("%Y-%m-%d")
		})
		Group("test").send({
			"text": json.dumps({'code': 'info message', 'sender': 'system', 'context': slip_message_info})
			})

@channel_session
def test_chat_connect(message):
	Group("chat").add(message.reply_channel)
	message.reply_channel.send({
		"accept": True
		})
	

@channel_session_user
def test_chat_disconnect(message):
	Group("chat").discard(message.reply_channel)

@channel_session_user
def test_chat_message(message):
	print(message.content['text'])
	message_dict = json.loads(message.content['text'])
	print(message_dict)

	Group("chat").send({
		"text": message.content['text'],
		})

def test_http_consumer(request):
	print("HELLO THIS IS HTTP")
	print(request)