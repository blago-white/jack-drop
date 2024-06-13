from django.urls import re_path

from .consumers.battle import BattleRequestAsyncConsumer

websocket_urlpatterns = [
    re_path(r'^ws/battle/(?P<initiator_id>\d+)/$',
            BattleRequestAsyncConsumer.as_asgi(),
            name="ws-battle"),
]
