from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^chat/ws/$', consumers.ChatConsumer.as_asgi(), name="ws-chat"),
]
