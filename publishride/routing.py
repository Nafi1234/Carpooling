from django.urls import path
from .consumer import RideConsumer

websocket_urlpatterns = [
    path('ws/ride/<str:room_name>/', RideConsumer.as_asgi()),
]
