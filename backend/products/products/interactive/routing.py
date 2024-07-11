from django.urls import re_path

from .consumers.battle import BattleRequestConsumer
from .consumers.feed.feed import FeedWebsocketConsumer

websocket_urlpatterns = [
    re_path(r'^products/ws/battle/$',
            BattleRequestConsumer.as_asgi(),
            name="ws-battle"),
    re_path(r'^products/ws/feed/$',
            FeedWebsocketConsumer.as_asgi(),
            name="ws-feed"),
]
