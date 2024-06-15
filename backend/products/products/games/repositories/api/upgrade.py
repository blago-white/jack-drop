from rest_framework.exceptions import ValidationError

from games.api.services.upgrade import UpgradeService
from games.api.services.users import UsersApiService
from games.serializers.upgrade import UpgradeRequestApiViewSerializer
from inventory.services.inventory import InventoryService
from items.services.items import ItemService
from .base import BaseApiRepository


class UpgradeApiRepository(BaseApiRepository):
    default_api_service = UpgradeService()
    default_inventory_service = InventoryService()
    default_items_service = ItemService()
    default_users_service = UsersApiService()

    default_serializer_class = UpgradeRequestApiViewSerializer

    _inventory_service: InventoryService()
    _api_service: UpgradeService

    def __init__(self, *args,
                 inventory_service: InventoryService = None,
                 items_service: ItemService = None,
                 users_service: UsersApiService = None,
                 **kwargs):
        self._inventory_service = inventory_service or self.default_inventory_service
        self._items_service = items_service or self.default_items_service
        self._users_service = users_service or self.default_users_service

        super().__init__(*args, **kwargs)

    def make_upgrade(self, data: dict, user_funds: dict) -> dict:
        validated_data, user_funds = (
            self._validate_funds(data=data, user_funds=user_funds)
        )

        serialized = self._complete_serializer(
            data=validated_data, user_funds=user_funds
        )

        result = self._api_service.make_upgrade(
            serialized=serialized
        )

        if not result:
            self._commit_loss(
                validated_data=validated_data,
                user_funds=user_funds
            )
        else:
            self._commit_win(
                owner_id=user_funds.get("id"),
                item_id=validated_data.get("receive_item_id")
            )

        return {"success": result}

    def _commit_loss(self, validated_data: dict, user_funds: dict) -> None:
        if validated_data.get("granted_item_id"):
            self._inventory_service.remove_from_inventory(
                owner_id=user_funds.get("id"),
                item_id=validated_data.get("granted_item_id")
            )
        else:
            self._users_service.update_user_balance(
                user_id=user_funds.get("id"),
                delta_amount=-validated_data.get("granted_funds")
            )

    def _commit_win(self, owner_id: int, item_id: int) -> None:
        self._inventory_service.add_item(
            owner_id=owner_id,
            item_id=item_id
        )

    def _complete_serializer(
            self, data: dict, user_funds: dict
    ) -> UpgradeRequestApiViewSerializer:
        receive_item_price = self._items_service.get_price(
            item_id=data.get("receive_item_id")
        )

        if data.get("granted_item_id"):
            granted_item_price = self._items_service.get_price(
                item_id=data.get("granted_item_id")
            )
        else:
            granted_item_price = data.get("granted_funds")

        return self._api_service.default_endpoint_serializer_class(
            instance={
                "granted_funds": granted_item_price,
                "receive_funds": receive_item_price,
                "user_funds": user_funds,
                "site_funds": {
                    "site_active_funds_per_hour": 1000  # TODO: Make service
                }
            }
        )

    def _validate_funds(
            self, data: dict, user_funds: float
    ) -> tuple[dict, dict]:
        serialized = self._api_service.default_endpoint_serializer_class(
            data=data
        )

        serialized.is_valid(raise_exception=True)

        if serialized.data.get("granted_item_id"):
            if not self._inventory_service.check_ownership(
                owner_id=user_funds.get("id"),
                item_id=serialized.data.get("granted_item_id")
            ):
                raise ValidationError(
                    detail="Restricted access for this item, you are not owner",
                    code=403
                )

        elif serialized.data.get("granted_funds"):
            if displayed_balance < serialized.data.get("granted_funds"):
                raise ValidationError(
                    "There are not enough balance funds for action"
                )

        return data, user_funds
