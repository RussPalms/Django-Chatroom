# this will be using more advanced routing such as relative path
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # the w+ says that anything after the chat/ is going to be recognized and picked up
    # very important to add '.as_asgi()' to the end when working with django 3
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
]