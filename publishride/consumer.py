from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Notification
from user.models import User


class RideConsumer(AsyncWebsocketConsumer):
   



    
    
    
    async def connect(self):
    

        print("entered in the consumer")
        
        await self.accept()
        print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_name = f"user_{self.scope['user'].id}"
        print(self.room_name,"room name")

        self.room_group_name = f"chat_{self.room_name}"

        print("here.........",self.room_group_name)
        
       

        
        

        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        

    async def disconnect(self,close_code):
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        
    @database_sync_to_async
    def get_user(self, user_id):
        print("Here giving the user_id",user_id)
        return User.objects.get(id=user_id)
    
    @database_sync_to_async
    def save_message(self, message_content, sender, receiver):
        message = Notification.objects.create(sender=sender, receiver=receiver, content=message_content, timestamp=timezone.now())
        message.save()
    async def receive(self, text_data):
        print("enteres")
        text_data_json = json.loads(text_data)

        message_type = text_data_json['type']
        print("inside the ride_approved sfddsffsgfsg@@@@@@@@@@@@@@@")

        if message_type == 'ride_approved':
            ride_id = text_data_json['rideId']
            message = text_data_json['message']

            group_name = f"ride_{ride_id}"
    
        # Use 'await' here to wait for the asynchronous method to complete
            await self.save_message(message, sender=self.scope['user'], receiver=None)

            await self.channel_layer.group_send(
            group_name,
            {
                'type': 'ride_approved',
                'ride_id': ride_id,
                'message': message,
            }
        )


    
   


   