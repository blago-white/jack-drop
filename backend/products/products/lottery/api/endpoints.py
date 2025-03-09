from rest_framework.generics import RetrieveAPIView, CreateAPIView

from common.mixins.api import ApiViewMixin



class GetCurrentLotteryApiView(RetrieveAPIView, ApiViewMixin):
    repository = None

    def retrieve(self, request, *args, **kwargs):
        ...


class ParticipateLotteryApiView(CreateAPIView):
    repository = None

    def create(self, request, *args, **kwargs):
        ...
