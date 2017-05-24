from django.contrib import admin
from .models import ChattingRoom, ChattingMessage

# Register your models here.
admin.site.register(ChattingRoom)
admin.site.register(ChattingMessage)
