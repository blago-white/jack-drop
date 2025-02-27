from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from common.api.default import DefaultApiView
from ..repository.discount import DiscountRepository
from ..repository.offers import PersonalOffersRepository


class PromocodeDiscountView(DefaultApiView):
    repository = DiscountRepository()
    serializer_class = repository.default_serializer_class

    def retrieve(self, request: Request, *args, **kwargs):
        return Response(
            data=self.repository.get(promocode=request.data.get("promocode"))
        )


class PersonalOffersView(DefaultApiView):
    repository = PersonalOffersRepository()
    serializer_class = repository.default_serializer_class
    http_method_names = ["get"]

    def retrieve(self, request: Request, *args, **kwargs):
        return Response(
            data=self.repository.get(client_id=request.user.id)
        )
