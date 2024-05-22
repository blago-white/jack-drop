from rest_framework.generics import RetrieveAPIView

from common.mixins.api import DetailedApiViewMixin
from ..repositories.items import ItemPriceRepository


class ItemPriceApiView(DetailedApiViewMixin, RetrieveAPIView):
    pk_url_kwarg = "item_id"
    repository = ItemPriceRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get_price(
                item_id=self.get_requested_pk()
            )
        )
