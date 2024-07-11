from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response


class BaseCreateApiView(CreateAPIView):
    _reponse_class = Response

    def get_queryset(self):
        return

    def _get_201_response(self, data=None) -> Response:
        return self._reponse_class(
            data=data,
            status=201
        )


class BaseRetrieveApiView(RetrieveAPIView):
    _response_class = Response

    def _get_200_response(self, data=None) -> Response:
        return self._response_class(data=data, status=200)
