from rest_framework.response import Response


class BaseRetrieveApiViewMixin:
    _response_class: Response = Response

    def get_200_request(self, data: dict):
        return self._response_class(
            data=data,
            status=200
        )
