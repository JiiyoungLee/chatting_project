from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from .models import ChattingRoom, ChattingMessage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import UserForm, UserNameForm, MakeRoomForm, ChattingMessageForm
from django.views import View
from django.views.generic import ListView
import os

# Create your views here.
def index(request):
	form = UserForm()
	context = { 'form' : form }
	return render(request, 'chatting/index.html', context)

def login_view(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		print("login!")
		login(request, user)
		return HttpResponseRedirect(reverse('chatting:room_list'))
	else:
		print("fail!")
		return HttpResponseRedirect(reverse('chatting:index'))

class SignInView(View):
	template_name = 'chatting/signin.html'

	def get(self, request):
		form = UserForm()
		context = {'form': form}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserForm(request.POST)
		User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
		return HttpResponseRedirect(reverse('chatting:index'))

"""
class RoomListView(ListView):
	template_name = 'chatting/rooms.html'
	model = ChattingRoom

	def get_context_data(self, **kwargs):
		context = super(RoomListView, self).get_context_data(**kwargs)
		
		this_user = User.objects.get(id=self.request.user.id)
		self.request.session['user'] = this_user.username
		
		#context['form'] = form
		return context
"""
class RoomListView(View):
	template_name = 'chatting/rooms_test.html'

	def get(self, request):
		this_user = User.objects.get(id=request.user.id)
		request.session['user'] = this_user.username
		return render(request, self.template_name)

class MakeRoomView(View):
	template_name = 'chatting/makeroom.html'

	def get(self, request):
		#if room number doesn't exist, then get request would be blocked.
		form = MakeRoomForm()
		context = {'form': form}
		return render(request, self.template_name, context)

	def post(self, request):
		form = MakeRoomForm(request.POST)
		new_instance = form.save()
		return HttpResponseRedirect(reverse('chatting:chatting', args=[new_instance.id]))

class ChattingView(View):
	template_name = 'chatting/room.html'

	def get(self, request, *args, **kwargs):
		room_id = kwargs['room_id']
		this_room = ChattingRoom.objects.get(id=room_id)
		this_room.member.add(request.user)
		this_room.save()
		chatting_messages = ChattingMessage.objects.filter(chatting_room_id=room_id)
		form = ChattingMessageForm()
		context = {'form': form, 'chatting_messages': chatting_messages, 'room': this_room.id }
		return render(request, self.template_name, context)

class ExitRoomView(View):
	template_name = 'chatting/rooms.html'

	def get(self, request, *args, **kwargs):
		print("EXIT")
		room_id = kwargs['room_id']
		this_room = ChattingRoom.objects.get(id=room_id)
		this_room.member.remove(request.user)
		this_room.save()
		return HttpResponseRedirect(reverse('chatting:room_list'))