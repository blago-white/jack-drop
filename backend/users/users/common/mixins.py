from rest_framework.response import Response


class DetailedApiViewMixin:
    pk_url_kwarg: str
    _response_class: Response = Response

    def get_requested_pk(self) -> int:
        return self.kwargs.get(self.pk_url_kwarg)

    def get_requested_pk_body(self) -> int:
        return self.request.dataww.get(self.pk_url_kwarg)


class BaseRetrieveApiViewMixin(DetailedApiViewMixin):
    def get_200_response(self, data: dict) -> Response:
        return self._response_class(
            data=data,
            status=200
        )


class BaseDetailedCreateApiViewMixin(DetailedApiViewMixin):
    def get_201_response(self, data: dict) -> Response:
        return self._response_class(
            data=data,
            status=201
        )
