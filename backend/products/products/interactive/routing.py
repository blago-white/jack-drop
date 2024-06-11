from django.urls import re_path

from .consumers.battle import BattleAsyncConsumer

websocket_urlpatterns = [
    re_path(r'^ws/battle/$', BattleAsyncConsumer.as_asgi(), name="ws-battle"),
]
