from rest_framework import generics
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class ChatCreateView(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    
class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer