from common.mixins.api import CreateApiViewMixin
from games.repositories.api.upgrade import UpgradeApiRepository
from games.repositories.api.users import UsersApiRepository
from games.serializers.upgrade import UpgradeRequestApiViewSerializer

from .base import BaseGameProxyCreateApiView


class UpgradeGameApiView(CreateApiViewMixin, BaseGameProxyCreateApiView):
    users_api_repository = UsersApiRepository()
    upgrade_repository = UpgradeApiRepository()
    serializer_class = UpgradeRequestApiViewSerializer

    def create(self, request, *args, **kwargs):
        user_funds = self.users_api_repository.get(
            user_request=request
        )

        result = self.upgrade_repository.make_upgrade(
            data=request.data | user_funds,
            user_funds=user_funds
        )

        return self.get_201_response(data=result)
