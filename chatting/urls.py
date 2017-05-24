from django.conf.urls import url, include
from django.contrib import admin
from chatting import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/lgoin$', views.login_view, name='login'),
    url(r'^user/signin$', views.SignInView.as_view(), name='signin'),
    url(r'^room/lists$', views.RoomListView.as_view(), name='room_list'),
    url(r'^room/make$', views.MakeRoomView.as_view(), name='make_room'),
    url(r'^room/enter/(?P<room_id>\d+)', views.ChattingView.as_view(), name='chatting'),
    url(r'^room/exit/(?P<room_id>\d+)', views.ExitRoomView.as_view(), name='exit_room'),
]
