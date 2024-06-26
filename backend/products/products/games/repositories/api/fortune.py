import json

from .base import BaseApiRepository

from games.api.services.forutne import (FortuneWheelPrizeApiService,
                                        FortuneWheelPrizeTypeApiService,
                                        PrizeTypes,
                                        GAME_SKIN_PRICE_RANGE,
                                        FREE_SKIN_PRICE_RANGE)
from games.api.services.site import SiteFundsApiService

from items.services.items import ItemService
from items.serializers import ItemSerializer

from inventory.models import Lockings
from inventory.services.inventory import InventoryService

from cases.services.cases import CaseService
from cases.serializers.items import CaseSerializer

from .users import UsersApiService


class FortuneWheelApiRepository(BaseApiRepository):
    default_api_service = None
    default_prize_api_service = FortuneWheelPrizeApiService()
    default_prize_type_api_service = FortuneWheelPrizeTypeApiService()
    default_site_funds_service = SiteFundsApiService()
    default_users_service = UsersApiService()

    default_items_service = ItemService()
    default_inventory_service = InventoryService()
    default_cases_service = CaseService()

    _LOCKINGS_FOR_PRIZE_TYPES = {
        PrizeTypes.FREE_SKIN: Lockings.UNLOCK,
        PrizeTypes.UPGRADE: Lockings.UPGRADE,
        PrizeTypes.CONTRACT: Lockings.CONTRACT
    }

    def __init__(
            self, *args,
            prize_api_service: FortuneWheelPrizeApiService = None,
            prize_type_api_service: FortuneWheelPrizeTypeApiService = None,
            site_funds_api_service: SiteFundsApiService = None,
            items_service: ItemService = None,
            cases_service: CaseService = None,
            users_service: CaseService = None,
            inventory_service: InventoryService = None,
            **kwargs):
        self._prize_api_service = (prize_api_service or
                                   self.default_prize_api_service)
        self._prize_type_api_service = (prize_type_api_service or
                                        self.default_prize_type_api_service)
        self._site_funds_service = site_funds_api_service or self.default_site_funds_service

        self._items_service = items_service or self.default_items_service
        self._cases_service = cases_service or self.default_cases_service
        self._users_service = users_service or self.default_users_service
        self._inventory_service = inventory_service or self.default_inventory_service

        super().__init__(*args, **kwargs)

    def make(self, user_data: dict):
        prize_type = self._get_prize_type(user_data=user_data)

        prize = self._get_prize(
            prize_type=prize_type,
            user_data=user_data,
            additional=self._get_additional(
                prize_type=prize_type
            )
        )

        self.commit(prize=prize, user_id=user_data.get("id"))

        return {"prize_type": prize_type.get("type"),
                "prize": prize.get("prize")}

    def commit(self, prize: dict, user_id: int) -> None:
        print(prize, "RESULT")

        if float(prize.get("site_funds_diff")):
            print(self._site_funds_service.update(prize.get(
                "site_funds_diff"
            )), "WOOOOOWWW")
        if float(prize.get("user_funds_diff")):
            pass
            # self._users_service.update_user_hiden_balance(
            #     user_id=user_id,
            #     delta_amount=float(prize.get("user_funds_diff"))
            # )

        prize_item = prize.get("prize")

        if (prize.get("type") in list(self._LOCKINGS_FOR_PRIZE_TYPES.keys())
                and prize_item):
            self._inventory_service.add_item(
                owner_id=user_id,
                item_id=prize_item.get("id"),
                locking=self._LOCKINGS_FOR_PRIZE_TYPES.get(
                    prize.get("type")
                )
            )

    def _get_additional(self, prize_type: str) -> dict:
        print(prize_type.get("type"))

        if prize_type.get("type") in list(
                self._LOCKINGS_FOR_PRIZE_TYPES.keys()):
            print("SEND ITEMS")
            return ItemSerializer(instance=self._items_service.get_all(
                *(FREE_SKIN_PRICE_RANGE
                  if prize_type == PrizeTypes.FREE_SKIN else
                  GAME_SKIN_PRICE_RANGE)
            ), many=True).data
        elif prize_type.get("type") == PrizeTypes.CASE_DISCOUNT:
            return CaseSerializer(instance=self._cases_service.get_all(),
                                  many=True)

        return {}

    def _get_prize(
            self, prize_type: str,
            user_data: dict,
            additional: dict = None) -> dict:
        serialized = self._prize_api_service.default_endpoint_serializer_class(
            data={
                "site_funds": {
                    "site_active_funds": self._site_funds_service.get(),
                },
                "user_funds": user_data,
                "type": prize_type.get("type"),
                "additional_data": json.dumps(additional or {})
            }
        )

        serialized.is_valid(raise_exception=True)

        return self._prize_api_service.make_prize(serialized=serialized)

    def _get_prize_type(self, user_data: dict) -> dict:
        serialized = (
            self._prize_type_api_service.default_endpoint_serializer_class(
                data={
                    "user_funds": {
                        "id": user_data.get("id"),
                        "user_advantage": user_data.get("user_advantage"),
                    },
                    "site_funds": {
                        "site_active_funds": self._site_funds_service.get()
                    },
                    "min_item_price": self._get_cheapest_item_price()
                }
            )
        )

        serialized.is_valid(raise_exception=True)

        return self._prize_type_api_service.get_prize_type(
            serialized=serialized
        )

    def _get_cheapest_item_price(self):
        return self._items_service.get_all()[0].price
