from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from .models import ChattingRoom, ChattingMessage, UserLogin
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, UserNameForm, MakeRoomForm, ChattingMessageForm, UserMessageForm
from django.views import View
from django.views.generic import ListView
import os, json

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
		user_instance, created = UserLogin.objects.get_or_create(
			user=user
			)
		user_instance.is_loggedin = 1
		user_instance.save()
		return HttpResponseRedirect(reverse('chatting:room_list'))
	else:
		print("fail!")
		return HttpResponseRedirect(reverse('chatting:index'))

@login_required
def logout_view(request):
	user_instance = UserLogin.objects.get(user=request.user)
	user_instance.is_loggedin = 0
	user_instance.save()
	logout(request)
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

	@method_decorator(login_required)
	def get(self, request):
		this_user = User.objects.get(id=request.user.id)
		request.session['user'] = this_user.username
		return render(request, self.template_name)

class MakeRoomView(View):
	template_name = 'chatting/makeroom.html'

	@method_decorator(login_required)
	def get(self, request):
		#if room number doesn't exist, then get request would be blocked.
		form = MakeRoomForm()
		context = {'form': form}
		return render(request, self.template_name, context)

	@method_decorator(login_required)
	def post(self, request):
		form = MakeRoomForm(request.POST)
		new_instance = form.save()
		return HttpResponseRedirect(reverse('chatting:chatting', args=[new_instance.id]))

class ChattingView(View):
	template_name = 'chatting/room.html'

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		room_id = kwargs['room_id']
		this_room = ChattingRoom.objects.get(id=room_id)
		this_room.member.add(request.user)
		this_room.save()
		members = User.objects.exclude(username=request.user.username).exclude(username='admin').exclude(is_active=0)
		#users = UserLogin.objects.exclude(user=request.user).exclude(user=User.objects.get(username='admin'))
		#print(users)
		chatting_form = ChattingMessageForm()
		message_form = UserMessageForm(initial={'sender': request.user})
		context = {'chatting_form': chatting_form, 'message_form': message_form, 'members': members, 'room': this_room.id }
		return render(request, self.template_name, context)

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		print(request.POST)
		"""sender = User.objects.get(username=request.POST['sender'])
		receiver = User.objects.get(username=request.POST['receiver'])
		context = request.POST['context']"""
		mutable = request.POST._mutable
		request.POST._mutable = True
		
		request.POST['receiver'] = User.objects.get(username=request.POST['receiver']).id
		request.POST._mutable = mutable
		print(request.POST)
		form = UserMessageForm(request.POST)
		instance = form.save()
		print(instance)		
		return HttpResponse(json.dumps({'result': instance.context }))

class ExitRoomView(View):
	template_name = 'chatting/rooms.html'

	def get(self, request, *args, **kwargs):
		room_id = kwargs['room_id']
		this_room = ChattingRoom.objects.get(id=room_id)
		this_room.member.remove(request.user)
		this_room.save()
		return HttpResponseRedirect(reverse('chatting:room_list'))



class MessageView(View):
	template_name = 'chatting/.html'

	"""@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		form = UserMessageForm(initial={'sender': request.user, 'receiver': User.objects.get(id=kwargs['receiver_id'])})
		context = { 'form': form }
		return render(request, self.template_name, context)
	"""

	
