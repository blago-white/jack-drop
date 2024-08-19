from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from ..repositories.base import BaseRepository


class BaseApiView:
    repository = BaseRepository
    _response_class = Response


class BaseCreateApiView(BaseApiView, CreateAPIView):
    def get_201_response(self, data: dict = None) -> Response:
        return self._response_class(data=data, status=201)
