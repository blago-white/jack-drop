from rest_framework.exceptions import ValidationError

from cases.services.items import CaseItemsService
from common.repositories.base import BaseRepository
from games.api.services.drop import CaseDropApiService
from games.api.services.site import SiteFundsApiService
from games.api.services.users import UsersApiService
from games.serializers.drop import DropCaseRequestSerializer, \
    DropItemSerializer
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

    _api_service: CaseDropApiService
    _site_funds_service: SiteFundsApiService

    def __init__(self, *args,
                 site_funds_service: SiteFundsApiService = None,
                 users_service: UsersApiService = None,
                 **kwargs) -> None:
        self._users_service = users_service or self.default_users_service
        self._site_funds_service = site_funds_service or self.default_site_funds_service

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
        )

        return {"dropped_item_id": drop_result.get("item_id")}

    def _commit_funds(self, case_data: dict,
                      user_funds: dict,
                      funds_delta: dict) -> None:
        # self._users_service.update_user_balance_by_id(
        #     delta_amount=-case_data.get("price") + funds_delta.get("user_funds_delta"),
        #     user_id=user_funds.get("id")
        # )
        # TODO: Uncomment

        self._site_funds_service.update(amount=funds_delta.get(
            "site_funds_delta"
        ))

    @staticmethod
    def _validate_user_balance(balance: float, case_price: int) -> bool:
        try:
            if float(balance) < float(case_price):
                raise ValidationError(
                    "There are not enough balance funds for action"
                )

        except:
            raise ValidationError("Not correct data")
