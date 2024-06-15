from django.urls import re_path

from .consumers.battle import BattleRequestAsyncConsumer

websocket_urlpatterns = [
    re_path(r'^products/ws/battle/$',
            BattleRequestAsyncConsumer.as_asgi(),
            name="ws-battle"),
]
