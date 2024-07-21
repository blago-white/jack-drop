from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository
from inventory.services.inventory import InventoryService
from games.api.services.users import UsersApiService

from ..services.sets import ItemSetService
from ..serializers import ItemsSetSerializer
from ..models.models import ItemsSet


class ItemsSetsRepository(BaseRepository):
    default_service = ItemSetService()
    default_inventory_service = InventoryService()
    default_users_service = UsersApiService()
    default_serializer_class = ItemsSetSerializer

    def __init__(self, *args,
                 inventory_service: InventoryService = None,
                 users_service: UsersApiService = None,
                 **kwargs):
        self._inventory_service = inventory_service or self.default_inventory_service
        self._users_service = users_service or self.default_users_service

        super().__init__(*args, **kwargs)

    def get_all(self) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(),
            many=True
        ).data

    def get(self, set_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get(set_id=set_id)
        ).data

    def buy(self, user_data: dict, set_id: int) -> dict:
        set_: ItemsSet = self._service.get(set_id=set_id)

        self._validate_balance(user_balance=user_data.get("displayed_balance"), set_=set_)

        self._users_service.update_user_balance_by_id(
            user_id=user_data.get("id"),
            delta_amount=-set_.price
        )

        created = self._inventory_service.bulk_add_item(
            items_ids=set_.items.all().values_list("pk", flat=True),
            owner_id=user_data.get("id")
        )

        return {"ok": bool(created)}

    def _validate_balance(self, user_balance: dict, set_: ItemsSet):
        if user_balance < set_.price:
            raise ValidationError("Not enought funds!")
