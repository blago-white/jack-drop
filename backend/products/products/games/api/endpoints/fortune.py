from django.views.decorators.csrf import csrf_exempt

from rest_framework.serializers import Serializer

from common.mixins.api import CreateAPIViewMixin
from .base import BaseGameProxyCreateApiView

from games.repositories.api.users import UsersApiRepository
from games.repositories.api.fortune import FortuneWheelApiRepository


class FortuneWheelGameApiView(CreateAPIViewMixin, BaseGameProxyCreateApiView):
    repository = FortuneWheelApiRepository()
    user_repository = UsersApiRepository()

    serializer_class = Serializer

    def create(self, request, *args, **kwargs):
        user_data = self.user_repository.get(user_request=request)

        return self.get_201_response(
            self.repository.make(user_data=user_data)
        )
