from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from ..repository.discount import DiscountRepository


class UserDiscountView(RetrieveAPIView):
    repository = DiscountRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "user_id"

    def retrieve(self, request, *args, **kwargs):
        return Response(
            data=self.repository.get(pk=self._get_user_id())
        )

    def _get_user_id(self):
        return self.kwargs.get(self.pk_url_kwarg)
