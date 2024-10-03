import json

from rest_framework.exceptions import ValidationError

from cases.serializers.items import CaseSerializer
from cases.services.cases import CaseService
from games.api.services.forutne import (FortuneWheelPrizeApiService,
                                        FortuneWheelPrizeTypeApiService,
                                        FortuneWheelTimeoutApiService,
                                        PrizeTypes,
                                        GAME_SKIN_PRICE_RANGE,
                                        FREE_SKIN_PRICE_RANGE)
from games.api.services.site import SiteFundsApiService
from bonus.services.bonus import BonusBuyService, UserBonusesService, BonusCaseService
from inventory.models import Lockings
from inventory.services.inventory import InventoryService
from items.serializers import ItemSerializer
from items.services.items import ItemService
from .base import BaseApiRepository
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
    default_bonus_service = BonusBuyService()
    default_user_bonus_service = UserBonusesService()
    default_bonus_case_service = BonusCaseService()

    default_timeout_service = FortuneWheelTimeoutApiService()

    _LOCKINGS_FOR_PRIZE_TYPES = {
        PrizeTypes.FREE_SKIN: Lockings.UNLOCK,
        PrizeTypes.UPGRADE: Lockings.UPGRADE,
        PrizeTypes.CONTRACT: Lockings.CONTRACT,
    }

    _BONUSE_COMMIT_METHODS: dict

    def __init__(
            self, *args,
            prize_api_service: FortuneWheelPrizeApiService = None,
            prize_type_api_service: FortuneWheelPrizeTypeApiService = None,
            site_funds_api_service: SiteFundsApiService = None,
            items_service: ItemService = None,
            cases_service: CaseService = None,
            users_service: CaseService = None,
            fortune_wheel_timeout_service: FortuneWheelTimeoutApiService = None,
            inventory_service: InventoryService = None,
            bonus_buy_service: BonusBuyService = None,
            user_bonus_service: UserBonusesService = None,
            bonus_case_service: BonusCaseService = None,
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
        self._bonus_service = bonus_buy_service or self.default_bonus_service
        self._user_bonus_service = user_bonus_service or self.default_user_bonus_service
        self._bonus_case_service = bonus_case_service or self.default_bonus_case_service

        self._timeout_service = (fortune_wheel_timeout_service or
                                 self.default_timeout_service)

        self._BONUSE_COMMIT_METHODS = {
            PrizeTypes.FREE_SKIN: self._user_bonus_service.add_free_item,
            PrizeTypes.UPGRADE: self._user_bonus_service.add_upgrade_item,
            PrizeTypes.CONTRACT: self._user_bonus_service.add_contract_item,
            PrizeTypes.CASE_DISCOUNT: self._user_bonus_service.add_discount
        }

        super().__init__(*args, **kwargs)

    def make(self, user_data: dict, promocode: str = None):
        timeout = int(
            self.get_timeout(user_id=user_data.get("id")).get("timeout")
        )

        if timeout and not promocode:
            raise ValidationError(
                detail=f"Timeout for next opening: {timeout} sec.",
                code=403
            )
        elif promocode and timeout:
            used = self._user_promo(
                user_id=user_data.get("id"),
                promocode=promocode
            )

            if not used:
                raise ValidationError(
                    detail=f"Given promocode does not exists!",
                    code=403
                )

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
        to_blogger_advantage = 0

        if float(prize.get("user_funds_diff")):
            ok, to_blogger_advantage = self._users_service.update_user_advantage(
                user_id=user_id,
                delta_advantage=float(prize.get("user_funds_diff"))
            )
        if float(prize.get("site_funds_diff")):
            self._site_funds_service.update(prize.get(
                "site_funds_diff"
            ) - to_blogger_advantage)

        prize_item, prize_data = prize.get("prize"), {}

        if (prize.get("type") in list(self._LOCKINGS_FOR_PRIZE_TYPES.keys())
                and prize_item):
            self._inventory_service.add_item(
                owner_id=user_id,
                item_id=prize_item.get("id"),
                locking=self._LOCKINGS_FOR_PRIZE_TYPES.get(
                    prize.get("type")
                )
            )

            prize_data = {
                "user_id": user_id,
                "item": self._items_service.get(
                    item_id=prize_item.get("id")
                )}

        elif prize.get("type") == PrizeTypes.CASE_DISCOUNT:
            bonus_case = self._bonus_case_service.create(
                case_id=prize_item.get("case").get("id"),
                discount=prize_item.get("discount")
            )

            prize_data = {
                "user_id": user_id,
                "bonus_case": bonus_case
            }

        self._BONUSE_COMMIT_METHODS.get(prize.get("type"))(**prize_data)

    def get_timeout(self, user_id: int) -> dict:
        serialized = self._timeout_service.default_endpoint_serializer_class(
            data={"user_id": user_id}
        )

        serialized.is_valid(raise_exception=True)

        return self._timeout_service.get(
            serialized=serialized
        )

    def _user_promo(self, user_id: int, promocode: str) -> bool:
        return self._prize_api_service.use_promocode(
            user_id=user_id,
            promocode=promocode
        )

    def _get_additional(self, prize_type: str) -> dict:
        if prize_type.get("type") in list(
                self._LOCKINGS_FOR_PRIZE_TYPES.keys()):
            return ItemSerializer(instance=self._items_service.get_all(
                *(FREE_SKIN_PRICE_RANGE
                  if prize_type == PrizeTypes.FREE_SKIN else
                  GAME_SKIN_PRICE_RANGE)
            ), many=True).data
        elif prize_type.get("type") == PrizeTypes.CASE_DISCOUNT:
            return CaseSerializer(instance=self._cases_service.get_paid(),
                                  many=True).data

        return {}

    def _get_prize(
            self, prize_type: str,
            user_data: dict,
            additional: dict = None) -> dict:
        print("ADDITIONAL", additional)

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
