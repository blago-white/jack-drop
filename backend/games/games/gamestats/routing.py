from django.urls import re_path
from .consumers.stats import GamesStatsConsumer

websocket_urlpatterns = [
   re_path(r'games/ws/stats/$', GamesStatsConsumer.as_asgi()),
]
