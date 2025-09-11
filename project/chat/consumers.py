import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_messages(self):
        qs = Message.objects.filter(chat_id=self.chat_id).order_by('created_at')
        return [
            {
                'id': message.id,
                'sender': message.sender.username,
                'content': message.content,
                'created_at': message.created_at.isoformat()
            } for message in qs
        ]

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get('content', '')

        message = await self.create_message(content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                    'created_at': message.created_at.isoformat()
                }
            }
        )

    @database_sync_to_async
    def create_message(self, content):
        user = self.scope['user']
        chat = Chat.objects.get(id=self.chat_id)
        print(f"Saving message: user={user}, chat={chat}, content={content}")
        return Message.objects.create(chat=chat, sender=user, content=content)

    

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
