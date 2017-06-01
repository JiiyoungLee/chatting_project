from django.contrib import admin
from .models import ChattingRoom, ChattingMessage, UserLogin

# Register your models here.
admin.site.register(ChattingRoom)
admin.site.register(ChattingMessage)
admin.site.register(UserLogin)
