from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..repositories.base import BaseRepository


class BaseApiView(APIView):
    repository = BaseRepository
    _response_class = Response

    def get_200_response(self, data: dict = None) -> Response:
        return self._response_class(data=data, status=200)


class BaseCreateApiView(BaseApiView, CreateAPIView):
    def get_201_response(self, data: dict = None) -> Response:
        return self._response_class(data=data, status=201)
