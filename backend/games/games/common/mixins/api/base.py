from rest_framework.response import Response


class ApiViewMixin:
    _response_class: Response = Response

    def get_200_response(self, data: dict):
        return self._response_class(
            data=data,
            status=200
        )
