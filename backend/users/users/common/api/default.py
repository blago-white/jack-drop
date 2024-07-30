from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from common.mixins import BaseRetrieveApiViewMixin, BaseDetailedCreateApiViewMixin
from common.repositories import BaseRepository


class DefaultApiView(APIView):
    repository: BaseRepository
    _response_class: Response = Response

    def get_queryset(self):
        return

    def get_400_response(self, data: dict = None) -> Response:
        return self._response_class(
            data=data,
            status=400
        )

    def get_200_response(self, data: dict = None) -> Response:
        return self._response_class(
            data=data,
            status=200
        )


class DefaultRetrieveApiView(BaseRetrieveApiViewMixin,
                             RetrieveAPIView,
                             DefaultApiView):
    pass


class DefaultCreateApiView(CreateAPIView,
                           DefaultApiView):
    pass


class DefaultUpdateApiView(BaseDetailedCreateApiViewMixin,
                           DefaultApiView,
                           UpdateAPIView):
    pass
