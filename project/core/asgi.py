import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.base")

django_asgi_app = get_asgi_application()

from chat.routing import websocket_urlpatterns  
from chat.middleware import JwtAuthMiddlewareStack 

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JwtAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})