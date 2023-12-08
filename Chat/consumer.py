import json
from django.db.models import Q
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chat
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from rest_framework_simplejwt.tokens import AccessToken
from .models import Chat
import json
from channels.db import database_sync_to_async
from django.utils import timezone
from user.models import User
import logging

logger = logging.getLogger(__name__)



class ChatRoomConsumer(AsyncWebsocketConsumer):
    

    async def connect(self):
        logger.info("WebSocket connection established")

        print("entered in the consumer")
        
        await self.accept()
        print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_name = f"user_{self.scope['user'].id}"
        print(self.room_name,"room name")

        self.room_group_name = f"chat_{self.room_name}"

        print("here.........",self.room_group_name)
        
       

        
        

        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # await self.accept()

    async def disconnect(self,close_code):
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        
    @database_sync_to_async
    def get_user(self, user_id):
        print("Here giving the user_id",user_id)
        return User.objects.get(id=user_id)
    
    @database_sync_to_async
    def save_message(self, message_content, sender, receiver):
        message = Chat.objects.create(sender=sender, receiver=receiver, content=message_content, timestamp=timezone.now())
        message.save()

    async def receive(self, text_data = None):
        print(text_data,'jhwgfwejfbwekhfgwejfbweh')
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        sender_id = text_data_json["sender"]
        receiver_id = text_data_json["recipient"]
        
        
        
        sender = await self.get_user(sender_id)
        receiver = await self.get_user(receiver_id)
        print(message_content,sender,receiver,"hereeeeee")

   
        await self.save_message(message_content, sender, receiver)
        await self.channel_layer.group_send(
        self.room_group_name, {"type": "chat.message", "message": message_content, "sender": sender, "receiver": receiver}
    )
        
        # message = ChatMessage.objects.create(sender=sender, receiver=receiver, content=message_content,timestamp=timezone.now())

        # message.save()

        # Send message to user's personal chat group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message_content, "sender": sender,"receiver ":receiver}
        )


    
    # async def save_message(self, message_content, sender, receiver):
    
    #     message = ChatMessage.objects.create(sender=sender, receiver=receiver, content=message_content, timestamp=timezone.now())
    #     message.save()


    async def chat_message(self, event):
        message_content = event["message"]
        sender = event["sender"]
        # receiver = event["receiver"]

        sender_data = {'id': sender.id, 'email': sender.email} 
        # receiver_data = {'id': receiver.id, 'email': receiver.email} 
        # print(receiver_data)
        
        await self.send(text_data=json.dumps({"type": "message", "message": message_content, "sender": sender_data}))


        # Send message to WebSocket
        # await self.send(text_data=json.dumps({"type":"message","message": message_content, "sender": sender,"receiver":receiver}))

