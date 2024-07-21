from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from games.api.services.users import UsersApiService
from ..services.api.withdraw import WithdrawScheduleApiService

from ..models import Lockings
from ..services.inventory import InventoryService
from ..serializers import InventoryItemSerializer


class InventoryRepository(BaseRepository):
    default_service = InventoryService()
    default_users_api_service = UsersApiService()
    default_schedule_service = WithdrawScheduleApiService()

    default_serializer_class = InventoryItemSerializer

    _service: InventoryService

    def __init__(
            self, *args,
            users_api_service: UsersApiService = None,
            schedule_service: WithdrawScheduleApiService = None,
            **kwargs):
        self._schedule_service = schedule_service or self.default_schedule_service
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
        item = self._service.get_item(inventory_item_id=item_id)

        ok = self._service.remove_from_inventory(owner_id=user_id,
                                                 inventory_item_id=item_id)

        if ok:
            self._users_api_service.update_user_balance_by_id(
                user_id=user_id,
                delta_amount=item.item.price
            )

        return {"ok": ok}

    def withdraw(self, user_data: int, item_id: int) -> dict:
        print(user_data, item_id, "_)DDDD")

        if not self._service.check_ownership(owner_id=user_data.get("id"),
                                             inventory_item_id=item_id):
            raise ValidationError("You not owner of item!")

        item = self._service.get_item(inventory_item_id=item_id)

        if item.locked_for != Lockings.UNLOCK:
            print("LOCKED")

            raise ValidationError("Item locked!")

        serialized = self._schedule_service.default_endpoint_serializer_class(
            data=dict(
                inventory_item_id=item_id,
                inventory_item_hash_name=item.item.market_hash_name,
                owner_trade_link=user_data.get("trade_link"),
                item_price=item.item.price,
            )
        )

        serialized.is_valid(raise_exception=True)

        success = self._schedule_service.add(serialized=serialized)

        if success:
            self._service.freeze_inventory_item(owner_id=user_data.get("id"),
                                                item_id=item_id)

        return {"ok": success}

    def commit_withdraw_results(self, results: dict):
        error = results.get("error_items_ids")
        success = results.get("error_items_ids")

        self._service.bulk_unfreeze(items_ids=error)

        self._service.bulk_remove_from_inventory(
            inventory_items_ids=success
        )
