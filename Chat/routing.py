from django.urls import re_path,path

from .import consumer

websocket_urlpatterns = [
    path('/chat/<str:room_name>/',consumer.ChatRoomConsumer.as_asgi())
    ]
