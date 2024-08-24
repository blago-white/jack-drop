from rest_framework.views import APIView
from rest_framework.response import Response

from common.api.default import DefaultApiView
from ..repository.discount import DiscountRepository


class PromocodeDiscountView(DefaultApiView):
    repository = DiscountRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request, *args, **kwargs):
        return Response(
            data=self.repository.get(promocode=request.data.get("promocode"))
        )
