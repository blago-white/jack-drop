import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'common.settings')
django.setup()

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from message import routing


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([*routing.websocket_urlpatterns])
    )
})
