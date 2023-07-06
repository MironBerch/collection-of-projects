from django.urls import re_path
from chat.consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(
        '/users/<user_id>/chat/',
        ChatConsumer.as_asgi()
    ),
]
