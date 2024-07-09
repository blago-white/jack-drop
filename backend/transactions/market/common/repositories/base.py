from abc import ABCMeta


class BaseRepository(metaclass=ABCMeta):
    _service: BaseModelService
    _serializer_class: serializers.Serializer
    default_service: BaseModelService | None
    default_serializer_class: serializers.Serializer | None

    def __init__(self,
                 service: BaseModelService = None,
                 serializer_class: serializers.Serializer = None
                 ):
        self._service = service or self.default_service
        self._serializer_class = (serializer_class or
                                  self.default_serializer_class)

