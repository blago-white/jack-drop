from .base import ApiViewMixin


class DetailedApiViewMixin(ApiViewMixin):
    pk_url_kwarg: str

    def get_requested_pk(self) -> int:
        return self.kwargs.get(self.pk_url_kwarg)
