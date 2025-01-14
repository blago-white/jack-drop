from django.urls import re_path

from .consumers.battle import BattleRequestConsumer

websocket_urlpatterns = [
    re_path(r'^products/ws/battle/$',
            BattleRequestConsumer.as_asgi(),
            name="ws-battle"),
]
