from common.views.api import BaseListAPIView

from games.repositories.api.users import UsersApiRepository
from ..repositories.inventory import InventoryRepository


class InventoryItemsListApiView(BaseListAPIView):
    _repository = InventoryRepository()
    _users_repository = UsersApiRepository()

    def list(self, request, *args, **kwargs):
        user_id = self._users_repository.get(
            user_request=request
        ).get("id")

        return self.get_200_response(
            data=self._repository.get_all(user_id=user_id)
        )
