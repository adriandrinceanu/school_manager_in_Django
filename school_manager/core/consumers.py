from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_username(self):
        # Check if user information is already stored in the connection object
        if hasattr(self, 'user'):
            return self.user.username

        # If not stored, retrieve it from the database using sync_to_async
        from django.contrib.auth.models import User
        user = User.objects.get(pk=self.scope['user'].pk)
        return user.username
    
    async def connect(self):
        from .models import Message 
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Accept the WebSocket connection
        await self.accept()
        
        # Load past messages from the database
        past_messages = await sync_to_async(Message.objects.filter)(room_name=self.room_name)
        past_messages = await sync_to_async(list)(past_messages.order_by('timestamp'))
        
        for message in past_messages:
            username = await self.get_username()
            await self.send(text_data=json.dumps({
                'message': message.content,
                'username': username,
                'timestamp': str(message.timestamp),
            }))

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    
        
    async def chat_message(self, event):
        # This method is called whenever a 'chat_message' is received
        message = event['message']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Save the message to the database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    @sync_to_async    
    def save_message(self, message):
        from .models import Message 
        user = self.scope["user"]
        if user.is_authenticated:
            Message.objects.create(user=user, content=message, room_name=self.room_name)
        else:
            print("Error: Unauthenticated user")
        
    # @sync_to_async
    # def save_message(self, message):
    #     from .models import Message 
    #     user = self.scope["user"]
    #     Message.objects.create(user=user, content=message, room_name=self.room_name)