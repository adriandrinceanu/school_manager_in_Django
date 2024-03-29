from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import logging
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturaltime



logger = logging.getLogger(__name__)


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
        self.room_name = self.scope['url_route']['kwargs']['username'] + '_' + self.scope['url_route']['kwargs']['username2']
        self.room_group_name = 'chat_%s' % self.room_name
        logger.info(f"Room group: {self.room_group_name}")
        # Accept the WebSocket connection
        await self.accept()
        
        # Load past messages from the database
        past_messages = await sync_to_async(Message.objects.filter)(chat_id=self.room_name)
        past_messages = await sync_to_async(list)(past_messages.order_by('timestamp'))
        
        
        for message in past_messages:
            # username = await self.get_username() #old username retrieval. it returned the current username of the logged user.
            username = message.username   # Get the username from the message
            timestamp = str(naturaltime(message.timestamp))  #Convert the timestamp to natural time
            await self.send(text_data=json.dumps({
                'message': message.content,
                'username': username,
                'timestamp': timestamp
            }))
        logger.info(f"Connected to {self.room_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Joined room group: {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Left room group: {self.room_group_name}")
    
        
        
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']  #Extract the username
        
        # Save the message to the database
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        logger.info(f"Received message: {message}")
        
    async def chat_message(self, event):
        # This method is called whenever a 'chat_message' is received
        message = event['message']
        # username = self.scope["user"].username # for selfkeeping
        username = event['username']
        now = datetime.now()
        
         # Humanize the timestamp
        timestamp = str(naturaltime(now))

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
        logger.info(f"Sending message: {message}")

        
        
    @sync_to_async    
    def save_message(self, username, message):
        from .models import Message 
        from django.contrib.auth.models import User
        # user = self.scope["user"]
        user = User.objects.get(username=username)
        if user.is_authenticated:
            Message.objects.create(user=user, username=username, content=message, chat_id=self.room_name)  # Add username=username
        else:
            print("Error: Unauthenticated user")
        
    # @sync_to_async
    # def save_message(self, message):
    #     from .models import Message 
    #     user = self.scope["user"]
    #     Message.objects.create(user=user, content=message, room_name=self.room_name)