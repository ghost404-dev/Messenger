from django.urls import path
from .views import ChatCreateView

urlpatterns = [
    path("", ChatCreateView.as_view(), name="chat-create"),
]
