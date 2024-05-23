from rest_framework.response import Response


class ApiViewMixin:
    _response_class: Response = Response

    def get_200_response(self, data: dict):
        return self._response_class(
            data=data,
            status=200
        )


class DetailedApiViewMixin(ApiViewMixin):
    pk_url_kwarg: str

    def get_requested_pk(self) -> int:
        return self.kwargs.get_user_info(self.pk_url_kwarg)


class CreateApiViewMixin(ApiViewMixin):
    def get_201_response(self, data: dict):
        return self._response_class(
            data=data,
            status=201
        )
