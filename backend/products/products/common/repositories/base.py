from abc import ABCMeta

from rest_framework.serializers import Serializer

from ..services.base import BaseReadOnlyService


class BaseRepository(metaclass=ABCMeta):
    _service: BaseReadOnlyService
    _serializer_class: Serializer
    default_service: BaseReadOnlyService | None
    default_serializer_class: Serializer | None

    def __init__(self,
                 service: BaseReadOnlyService = None,
                 serializer_class: Serializer = None
                 ):
        self._service = service or self.default_service
        self._serializer_class = (serializer_class or
                                  self.default_serializer_class)
