from django.http import HttpResponse
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import ChattingRoom
from django.contrib.auth.models import User
from django.core import serializers
from collections import OrderedDict
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
	print("@@@disconnect")
	Group("test").discard(message.reply_channel)

@channel_session
def test_message(message):
	print(message.content['text'])
	message_dict = json.loads(message.content['text'])
	print(message_dict)

	Group("test").send({
		"text": message.content['text'],
		})
