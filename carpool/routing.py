from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django
django.setup()
import Chat.routing 

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(  
        URLRouter(
           Chat.routing.websocket_urlpatterns
        )
    ),
})