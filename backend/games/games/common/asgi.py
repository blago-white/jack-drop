import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')

from django import setup

setup()

from gamestats import routing

application = ProtocolTypeRouter({
   "http": get_asgi_application(),
   "websocket": URLRouter(
       routing.websocket_urlpatterns
   ),
})
