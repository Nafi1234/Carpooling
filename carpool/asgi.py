"""
ASGI config for carpool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""



#from Chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
#from publishride.routing import websocket_urlpatterns as ride_websocket_urlpatterns


#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carpool.settings')

#django_asgi_app = get_asgi_application()
#application = ProtocolTypeRouter({
#    'websocket': AuthMiddlewareStack(  
#        URLRouter(
 #          chat_websocket_urlpatterns+ride_websocket_urlpatterns
 #       )
  #  ),
 #    "http": django_asgi_app,
#})
#channel_layer = get_channel_layer() 
# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
import carpool.routing  
import django

django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carpool.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),  
    'websocket': carpool.routing.application,  
})
