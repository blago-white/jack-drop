from common.repositories.base import BaseRepository

from games.api.services.users import UsersApiService

from ..models import Lockings
from ..services.inventory import InventoryService
from ..serializers import InventoryItemSerializer


class InventoryRepository(BaseRepository):
    default_service = InventoryService()
    default_users_api_service = UsersApiService()
    default_serializer_class = InventoryItemSerializer

    _service: InventoryService

    def __init__(self, *args,
                 users_api_service: UsersApiService = None,
                 **kwargs):

        self._users_api_service = users_api_service or self.default_users_api_service

        super().__init__(*args, **kwargs)

    def get_all(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(user_id=user_id),
            many=True
        ).data

    def get_all_unlock(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(
                user_id=user_id, locked_for=Lockings.UNLOCK
            ),
            many=True
        ).data

    def get_all_for_contract(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(
                user_id=user_id, locked_for=Lockings.CONTRACT
            ) | self._service.get_all(
                user_id=user_id, locked_for=Lockings.UNLOCK
            ),
            many=True
        ).data

    def get_all_for_upgrade(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(
                user_id=user_id, locked_for=Lockings.UPGRADE
            ) | self._service.get_all(
                user_id=user_id, locked_for=Lockings.UNLOCK
            ),
            many=True
        ).data

    def get_count(self, user_id: int) -> dict[str, int]:
        return {
            "total": self._service.get_all(user_id=user_id).count(),
            "can_sell": self._service.get_all(
                user_id=user_id,
                locked_for=Lockings.UNLOCK
            ).count()
        }

    def sell(self, user_id: int, item_id: int) -> dict:  # TODO: Make
        return {"ok": True}

    def withdraw(self, user_id: int, item_id: int) -> dict:
        return {"ok": True}
