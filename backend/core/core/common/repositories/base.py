from rest_framework import serializers

from ..services.base import BaseService


class BaseRepository:
    default_service: BaseService
    default_serializer_class: serializers.Serializer

    def __init__(self, service: BaseService = None,
                 serializer_class: serializers.Serializer = None):
        self._service = service or self.default_service
        self._serializer_class = serializer_class or self.default_serializer_class
