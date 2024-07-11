from django.views.decorators.csrf import csrf_exempt

from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from common.mixins.api import CreateAPIViewMixin
from common.mixins.api import ApiViewMixin
from .base import BaseGameProxyCreateApiView

from games.serializers.fortune import WheelPrizeApiViewSerializer
from games.repositories.api.users import UsersApiRepository
from games.repositories.api.fortune import FortuneWheelApiRepository


class FortuneWheelGameApiView(CreateAPIViewMixin, BaseGameProxyCreateApiView):
    repository = FortuneWheelApiRepository()
    user_repository = UsersApiRepository()

    serializer_class = WheelPrizeApiViewSerializer

    def create(self, request, *args, **kwargs):
        user_data = self.user_repository.get(user_request=request)

        promocode = request.data.get("promocode")

        return self.get_201_response(
            self.repository.make(user_data=user_data,
                                 promocode=promocode)
        )


class FortuneWheelTimeoutApiView(ApiViewMixin, APIView):
    repository = FortuneWheelApiRepository()
    user_repository = UsersApiRepository()

    def get(self, request):
        user_id = self.user_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self.repository.get_timeout(user_id=int(user_id))
        )
