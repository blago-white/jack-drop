from django.db import transaction

from rest_framework.exceptions import ValidationError

from games.api.services.site import SiteFundsApiService
from games.api.services.upgrade import UpgradeService
from games.api.services.users import UsersApiService
from games.models import Games
from games.serializers.upgrade import UpgradeRequestApiViewSerializer
from games.services.result import GameResultService
from games.services.transfer import GameResultData
from inventory.services.inventory import InventoryService
from items.services.items import ItemService
from .base import BaseApiRepository


class UpgradeApiRepository(BaseApiRepository):
    default_api_service = UpgradeService()
    default_inventory_service = InventoryService()
    default_items_service = ItemService()
    default_users_service = UsersApiService()
    default_site_funds_service = SiteFundsApiService()
    default_game_result_service = GameResultService()

    default_serializer_class = UpgradeRequestApiViewSerializer

    _granted_amount: float = 0
    _receive_amount: float = 0

    _inventory_service: InventoryService()
    _api_service: UpgradeService
    _site_funds_service: SiteFundsApiService

    def __init__(self, *args,
                 site_funds_service: SiteFundsApiService = None,
                 inventory_service: InventoryService = None,
                 items_service: ItemService = None,
                 users_service: UsersApiService = None,
                 game_result_service: GameResultService = None,
                 serializer_class: UpgradeRequestApiViewSerializer = None,
                 **kwargs):
        self._inventory_service = inventory_service or self.default_inventory_service
        self._items_service = items_service or self.default_items_service
        self._users_service = users_service or self.default_users_service
        self._serializer_class = serializer_class or self.default_serializer_class
        self._site_funds_service = site_funds_service or self.default_site_funds_service
        self._game_result_service = game_result_service or self.default_game_result_service

        super().__init__(*args, **kwargs)

    @transaction.atomic()
    def make_upgrade(self, data: dict, user_funds: dict) -> dict:
        validated_data, user_funds = (
            self._validate_funds(data=data, user_funds=user_funds)
        )

        serialized = self._complete_serializer(
            data=validated_data, user_funds=user_funds
        )

        if validated_data.get("granted_item_id"):
            granted = self._inventory_service.get_item(
                inventory_item_id=validated_data.get("granted_item_id"),
            )

            if not granted:
                raise ValidationError("Cannot make upgrade with this item, "
                                      "please try later or other item!")
        else:
            granted = None

        self._inventory_service.remove_from_inventory(
            owner_id=user_funds.get("id"),
            inventory_item_id=validated_data.get("granted_item_id")
        )

        result = self._api_service.make_upgrade(
            serialized=serialized
        )

        if result:
            self._commit_win(
                validated_data=validated_data,
                owner_id=user_funds.get("id"),
                item_id=validated_data.get("receive_item_id"),
                user_funds=user_funds,
                granted=granted
            )
        else:
            self._commit_loss(
                validated_data=validated_data,
                user_funds=user_funds,
                granted=granted
            )

        if validated_data.get("granted_item_id"):
            self._game_result_service.save(data=GameResultData(
                user_id=user_funds.get("id"),
                is_win=bool(result),
                game=Games.UPGRADE,
                first_item_id=validated_data.get("receive_item_id"),
                second_item_id=granted.item.id
            ))
        else:
            self._game_result_service.save(data=GameResultData(
                user_id=user_funds.get("id"),
                is_win=bool(result),
                game=Games.UPGRADE,
                first_item_id=validated_data.get("receive_item_id"),
            ))

        return {"success": result}

    def _commit_loss(self, validated_data: dict,
                     user_funds: dict,
                     granted: "InventoryItem") -> None:
        if granted:
            item_price = granted.item.price

            ok, to_blogger_advantage = self._users_service.update_user_advantage(
                user_id=user_funds.get("id"),
                delta_advantage=-item_price
            )

            self._site_funds_service.increase(
                amount=to_blogger_advantage
            )

        elif validated_data.get("granted_funds"):
            self._users_service.update_user_balance_by_request(
                user_id=user_funds.get("id"),
                delta_amount=-validated_data.get("granted_funds")
            )
            
            ok, to_blogger_advantage = self._users_service.update_user_advantage(
                user_id=user_funds.get("id"),
                delta_advantage=-validated_data.get("granted_funds")
            )

            self._site_funds_service.increase(
                amount=to_blogger_advantage
            )

    def _commit_win(self, validated_data: dict,
                    user_funds: dict,
                    owner_id: int,
                    granted: "InventoryItem",
                    item_id: int) -> None:
        if validated_data.get("granted_item_id"):
            granted_funds = granted.item.price
        else:
            self._users_service.update_user_balance_by_request(
                user_id=user_funds.get("id"),
                delta_amount=-validated_data.get("granted_funds")
            )
            
            granted_funds = validated_data.get("granted_funds")

        if (granted_funds / self._receive_amount) > 0.98:
            raise ValidationError("Cannot make upgrade with < 98%")

        item = self._inventory_service.add_item(
            owner_id=owner_id,
            item_id=item_id
        )

        ok, to_blogger_advantage = self._users_service.update_user_advantage(
            user_id=user_funds.get("id"),
            delta_advantage=item.item.price - granted_funds
        )

        self._site_funds_service.update(
            amount=granted_funds - self._receive_amount - to_blogger_advantage,
        )

    def _complete_serializer(
            self, data: dict, user_funds: dict
    ) -> UpgradeRequestApiViewSerializer:
        self._receive_amount = self._items_service.get_price(
            item_id=data.get("receive_item_id")
        )

        if data.get("granted_item_id"):
            self._granted_amount = self._inventory_service.get_item(
                inventory_item_id=data.get("granted_item_id")
            ).item.price

        else:
            self._granted_amount = data.get("granted_funds")

        return self._api_service.default_endpoint_serializer_class(
            instance={
                "granted_funds": self._granted_amount,
                "receive_funds": self._receive_amount,
                "user_funds": user_funds,
                "site_funds": {
                    "site_active_funds": self._site_funds_service.get()
                }
            }
        )

    def _validate_funds(
            self, data: dict, user_funds: float
    ) -> tuple[dict, dict]:
        serialized = self._serializer_class(
            data=data | user_funds
        )

        serialized.is_valid(raise_exception=True)

        if serialized.data.get("granted_item_id"):
            if not self._inventory_service.check_ownership(
                owner_id=user_funds.get("id"),
                inventory_item_id=serialized.data.get("granted_item_id")
            ):
                raise ValidationError(
                    detail="Restricted access for this item, you are not owner",
                    code=403
                )

        elif serialized.data.get("granted_funds"):
            if user_funds.get("displayed_balance") < serialized.data.get(
                    "granted_funds"
            ):
                raise ValidationError(
                    "There are not enough balance funds for action"
                )

        return data, user_funds
