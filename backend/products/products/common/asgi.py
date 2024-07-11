import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')
django.setup()

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from interactive.auth import JWTTokenAuthMiddlewareStack
from interactive.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTTokenAuthMiddlewareStack(
        URLRouter([*websocket_urlpatterns])
    )
})
