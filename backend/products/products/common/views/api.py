from rest_framework.generics import ListAPIView

from ..repositories.base import BaseRepository


class BaseListAPIView(ListAPIView):
    _repository: BaseRepository

    def list(self, request, *args, **kwargs):
        return self.get_200_response(data=self._repository.get_all())
