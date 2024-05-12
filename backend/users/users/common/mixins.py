from rest_framework.response import Response


class BaseRetrieveApiViewMixin:
    pk_url_kwarg: str
    _response_class: Response = Response

    def get_200_request(self, data: dict) -> Response:
        return self._response_class(
            data=data,
            status=200
        )

    def get_requested_pk(self) -> int:
        return self.kwargs.get(self.pk_url_kwarg)
