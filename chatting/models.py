from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ChattingRoom(models.Model):
	MEMBERCOUNTCHOICE = (
		('2', 2),
		('3', 3),
		('4', 4),
	)
	
	creator = models.CharField(max_length=20)
	room_name = models.CharField(max_length=100, default='')
	member_count = models.CharField(max_length=1, choices=MEMBERCOUNTCHOICE)
	member = models.ManyToManyField(User)
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'room_name: ' + self.room_name + ' creator: ' + self.creator + ' member_count: ' + self.member_count

class ChattingMessage(models.Model):
	chatting_room = models.ForeignKey(ChattingRoom)
	sender = models.CharField(max_length=20)
	context = models.CharField(max_length=500)
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'sender: ' + self.sender + ' context: ' + self.context

