from abc import ABCMeta

from rest_framework.serializers import Serializer

from ..services import BaseService


class BaseRepository(metaclass=ABCMeta):
    _service: BaseService
    _serializer_class: Serializer
    default_service: BaseService | None
    default_serializer_class: Serializer | None

    def __init__(self,
                 service: BaseService = None,
                 serializer_class: Serializer = None
                 ):
        self._service = service or self.default_service
        self._serializer_class = (serializer_class or
                                  self.default_serializer_class)
