from django import forms
from django.forms import PasswordInput, TextInput, Textarea
from .models import ChattingRoom, ChattingMessage, UserMessage
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
			'password': PasswordInput
		}


class UserNameForm(forms.Form):
	user_name = forms.CharField(label='User Name', max_length=20)

class MakeRoomForm(forms.ModelForm):
	class Meta:
		model = ChattingRoom
		exclude = ['member', 'created_time', 'modified_time']

class ChattingMessageForm(forms.ModelForm):
	class Meta:
		model = ChattingMessage
		fields = ['sender', 'context']

class UserMessageForm(forms.ModelForm):
	class Meta:
		model = UserMessage
		exclude = ['created_time', 'modified_time', 'is_checked']
		widgets = {
			'sender': TextInput(attrs={'id': 'id_message_sender',}),
			'receiver': TextInput(attrs={'id': 'id_message_receiver',}),
			'context': Textarea(attrs={'id': 'id_message_context', 'cols': 40, 'rows': 5}),
		}

		