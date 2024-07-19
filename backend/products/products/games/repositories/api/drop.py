from rest_framework.exceptions import ValidationError

from cases.services.items import CaseItemsService
from common.repositories.base import BaseRepository
from games.api.services.drop import CaseDropApiService
from games.api.services.site import SiteFundsApiService
from games.api.services.users import UsersApiService
from games.serializers.drop import DropCaseRequestSerializer, \
    DropItemSerializer
from games.services.transfer import GameResultData
from games.services.result import GameResultService
from games.models import Games
from inventory.services.inventory import InventoryService

from .base import BaseApiRepository


class DropItemsRepository(BaseRepository):
    default_service = CaseItemsService()
    default_serializer_class = DropItemSerializer

    def get_drop_items_by_case(self, case_pk: str):
        return self._serializer_class(
            instance=self._service.get_drop_case_items_for_case(
                case_pk=case_pk
            ),
            many=True
        ).data


class CaseDropApiRepository(BaseApiRepository):
    default_endpoint_serializer_class = DropCaseRequestSerializer
    default_api_service = CaseDropApiService()
    default_site_funds_service = SiteFundsApiService()
    default_users_service = UsersApiService()
    default_inventory_service = InventoryService()
    default_game_results_service = GameResultService()

    _api_service: CaseDropApiService
    _site_funds_service: SiteFundsApiService
    _game_results_service: GameResultService

    def __init__(self, *args,
                 site_funds_service: SiteFundsApiService = None,
                 users_service: UsersApiService = None,
                 inventoy_service: InventoryService = None,
                 game_results_service: GameResultService = None,
                 **kwargs) -> None:
        self._users_service = users_service or self.default_users_service
        self._site_funds_service = site_funds_service or self.default_site_funds_service
        self._inventory_service = inventoy_service or self.default_inventory_service
        self._game_results_service = game_results_service or self.default_game_results_service

        super().__init__(*args, **kwargs)

    def drop(self, user_funds: dict, case_data: dict) -> dict:
        serialized: DropCaseRequestSerializer = (
            self._api_service.default_endpoint_serializer_class(
                data={
                    "case_id": case_data.get("id"),
                    "items": case_data.get("items"),
                    "funds": {
                        "user_advantage": user_funds.get("user_advantage"),
                        "site_active_funds": self._site_funds_service.get()
                    },
                    "price": case_data.get("price")
                }
            )
        )

        serialized.is_valid(raise_exception=True)

        self._validate_user_balance(
            balance=user_funds.get("displayed_balance"),
            case_price=serialized.data.get("price")
        )

        drop_result = self._api_service.drop(
            serialized=serialized.data
        )

        self._commit_funds(
            case_data=case_data,
            user_funds=user_funds,
            funds_delta=drop_result.get("funds"),
            dropped_item_id=drop_result.get("item").get("item_id")
        )

        return {"dropped_item": drop_result.get("item")}

    def _commit_funds(self, case_data: dict,
                      user_funds: dict,
                      funds_delta: dict,
                      dropped_item_id: int) -> None:
        # self._users_service.update_user_balance_by_id(
        #     delta_amount=-case_data.get("price") + funds_delta.get("user_funds_delta"),
        #     user_id=user_funds.get("id")
        # ) # TODO: ONLY ADVANTAGE

        self._users_service.update_user_balance_by_id(
            delta_amount=-case_data.get("price"),
            user_id=user_funds.get("id")
        )

        self._site_funds_service.update(amount=funds_delta.get(
            "site_funds_delta"
        ))

        self._inventory_service.add_item(owner_id=user_funds.get("id"),
                                         item_id=int(dropped_item_id))

        self._game_results_service.save(
            data=GameResultData(user_id=user_funds.get("id"),
                                is_win=True,
                                game=Games.DROP,
                                first_item_id=dropped_item_id,
                                case_id=case_data.get("id"))
        )

    @staticmethod
    def _validate_user_balance(balance: float, case_price: int) -> bool:
        if float(balance) < float(case_price):
            raise ValidationError(
                "There are not enough balance funds for action"
            )
