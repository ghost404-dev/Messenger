from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "is_group", "name", "participants"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "content", "created_at"]

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)