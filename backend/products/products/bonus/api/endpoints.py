from rest_framework.generics import CreateAPIView

from common.views.api import BaseRetreiveAPIView
from common.mixins.api import CreateAPIViewMixin

from ..repositories.bonus import BonusBuyRepository
from games.repositories.api.users import UsersApiRepository


class BonusBuyStatusApiView(BaseRetreiveAPIView):
    repository = BonusBuyRepository()
    users_repository = UsersApiRepository()

    def retrieve(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self.repository.get(user_id=user_id)
        )


class BonusBuyNextLevelApiView(CreateAPIViewMixin, CreateAPIView):
    _repository = BonusBuyRepository()
    users_repository = UsersApiRepository()

    def create(self, request, *args, **kwargs):
        user_id = self.users_repository.get(user_request=request).get("id")

        return self.get_200_response(
            data=self._repository.next_level(user_id=user_id)
        )
