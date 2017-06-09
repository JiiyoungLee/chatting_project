from django.contrib import admin
from .models import ChattingRoom, ChattingMessage, UserLogin, UserMessage

# Register your models here.
admin.site.register(ChattingRoom)
admin.site.register(ChattingMessage)
admin.site.register(UserLogin)
admin.site.register(UserMessage)
