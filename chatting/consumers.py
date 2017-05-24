from django.http import HttpResponse
from channels import Group
from channels.sessions import channel_session

@channel_session
def ws_message(message):
	print("receive")

	Group("chat-%s" % message.channel_session['room']).send({
		"text": message.content['text'],
	})

@channel_session
def ws_add(message):
	room_number = message.content['query_string'].split('=')[1]
	print(room_number)
	message.channel_session['room'] = room_number
	Group("chat-%s" % room_number).add(message.reply_channel)
	message.reply_channel.send({
		"accept": True
	})

@channel_session
def ws_disconnect(message):
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)