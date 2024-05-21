from rest_framework.request import Request

from common.repositories import BaseRepository
from common.services.api.items import ProductItemApiService
from common.services.api.users import UsersApiService
from common.states import FundsState
from ..serializers import GameRequestSerializer
from ..services.upgrade import UpgradeService


class UpgradeRepository(BaseRepository):
    default_service = UpgradeService()
    default_serializer_class = GameRequestSerializer
    _users_api_service = UsersApiService()
    _items_api_service = ProductItemApiService()
    _service: UpgradeService
    _serializer_class: GameRequestSerializer

    def __init__(self,
                 *args,
                 users_api_service: UsersApiService = None,
                 items_api_service: UsersApiService = None,
                 **kwargs):
        self._users_api_service = users_api_service or self._users_api_service
        self._items_api_service = items_api_service or self._items_api_service

        super().__init__(*args, **kwargs)

    def upgrade(self, request: Request) -> dict:
        user = self._users_api_service.get_info(
            user_request=request
        )

        serialized: GameRequestSerializer = self._serializer_class(request.DATA)

        serialized.is_valid(raise_exception=True)

        receive_amount = self._items_api_service.get_price(
            item_id=serialized.receive_item
        )

        Funds_state = FundsState(
            usr_advantage=user.advantage,
            site_active_hour_funds=1000  # TODO: Make service
        )

        if not serialized.granted_balance:
            granted_amount = self._items_api_service.get_price(
                item_id=serialized.granted_item
            )
        else:
            granted_amount = serialized.granted_balance

        upgrade_successful = self._service.make_upgrade(
            user_id=user,
            granted_amount=granted_amount,
            receive_amount=receive_amount,
            Funds_state=Funds_state
        )

        return {"success": upgrade_successful}
