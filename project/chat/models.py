from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    is_group = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name="chats")


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
