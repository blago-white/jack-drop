from django.conf import settings

from rest_framework.serializers import Serializer


class BaseApiService:
    default_routes: dict[str, str] = settings.GAMES_SERVICE_ROUTES
    default_endpoint_serializer_class: Serializer

    def __init__(self, routes: dict[str, str] = None,
                 endpoint_serializer_class: Serializer = None):
        self._routes = routes or self.default_routes
        self._endpoint_serializer_class = (endpoint_serializer_class or
                                           self.default_endpoint_serializer_class)

    @property
    def endpoint_serializer_class(self):
        return self._endpoint_serializer_class
