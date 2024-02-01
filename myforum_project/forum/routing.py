from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from forum.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
from django.urls import re_path
from . import consumers

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/chat/', ChatConsumer.as_asgi()),
            ]
        )
    ),
})

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]