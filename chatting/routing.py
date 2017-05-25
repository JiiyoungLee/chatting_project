from channels.routing import route
from .consumers import ws_message, ws_add, ws_disconnect, room_connect, room_disconnect, room_list_connect, room_list_disconnect, room_message

channel_routing = [
	route("websocket.connect", room_list_connect, path=r'^/list/$'),
	route("websocket.disconnect", room_list_disconnect, path=r'^/list/$'),
	route("websocket.connect", room_connect, path=r'^/test/$'),
	route("websocket.disconnect", room_disconnect, path=r'^/test/$'),
	route("websocket.receive", room_message, path=r'^/test/$'),
	route("websocket.receive", ws_message),
	route("websocket.connect", ws_add),
	route("websocket.disconnect", ws_disconnect),

	
]