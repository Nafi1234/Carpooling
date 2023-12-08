"""
ASGI config for carpool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer

from Chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from publishride.routing import websocket_urlpatterns as ride_websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carpool.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(  
        URLRouter(
           chat_websocket_urlpatterns+ride_websocket_urlpatterns
        )
    ),
     "http": get_asgi_application(),
})
channel_layer = get_channel_layer()