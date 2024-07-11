from .detail import DetailedApiViewMixin


class DeleteApiViewMixin(DetailedApiViewMixin):
    def get_204_response(self):
        return self._response_class(status=204)
