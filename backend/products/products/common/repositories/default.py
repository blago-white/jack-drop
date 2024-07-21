from abc import ABCMeta

from common.repositories.base import (BaseModelRepository, PrimaryKey,
                                      RequestPostData)


class DefaultRepository(BaseModelRepository, metaclass=ABCMeta):

    def get_all(self) -> dict:
        objects = self._service.get_all()
        serialized_objects = self._serializer(
            instance=objects,
            many=True
        )

        return serialized_objects.data

    def get(self, pk: PrimaryKey) -> dict:
        return self._serializer(instance=self._service.get(pk)).data

    def create(self, data: RequestPostData) -> dict:
        serializer = self._serializer(data=data)

        serializer.is_valid(raise_exception=True)

        serializer = self._serializer(
            instance=self._service.create(data=serializer.validated_data)
        )

        return serializer.data

    def update(self, pk: PrimaryKey, data: RequestPostData):
        serializer = self._serializer(data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_instance = self._service.update(pk=pk, data=serializer.validated_data)

        return self._serializer(instance=updated_instance).data

    def delete(self, pk: PrimaryKey) -> None:
        self._service.delete(pk=pk)
