from .base import ApiViewMixin


class CreateApiViewMixin(ApiViewMixin):
    def get_201_response(self, data: dict):
        return self._response_class(
            data=data,
            status=201
        )
