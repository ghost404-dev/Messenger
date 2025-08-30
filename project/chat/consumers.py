import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or isinstance(user, AnonymousUser):
            await self.close(code=4403)
            return

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        user = self.scope["user"]
        if not text_data:
            return
        data = json.loads(text_data)
        message = data.get("message")
        if not message:
            return
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "user_id": user.id,
                "username": getattr(user, "username", None),
                "message": message,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "user_id": event["user_id"],
            "username": event["username"],
            "message": event["message"],
        }))

    chat_message = chat_message