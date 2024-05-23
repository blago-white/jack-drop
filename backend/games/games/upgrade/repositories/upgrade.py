from rest_framework.request import Request

from common.repositories import BaseRepository
from common.states import FundsState
from ..serializers import UpgradeRequestSerializer
from ..services.upgrade import UpgradeService


class UpgradeRepository(BaseRepository):
    default_service = UpgradeService()
    default_serializer_class = UpgradeRequestSerializer
    _service: UpgradeService
    _serializer_class: UpgradeRequestSerializer

    def upgrade(self, request: Request) -> dict:
        serialized: UpgradeRequestSerializer = self._serializer_class(request.DATA)

        serialized.is_valid(raise_exception=True)

        receive_amount = serialized.data.get_user_info("receive_funds")

        funds_state = FundsState(
            usr_advantage=serialized.data.get_user_info("user_funds").get_user_info("advantage"),
            site_active_hour_funds=serialized.data.get_user_info("site_funds").get_user_info(
                "site_active_hour_funds"
            )
        )

        granted_amount = serialized.data.get_user_info("granted_funds")

        upgrade_successful = self._service.make_upgrade(
            user_id=serialized.data.get_user_info("user_funds").get_user_info("id"),
            granted_amount=granted_amount,
            receive_amount=receive_amount,
            funds_state=funds_state
        )

        return {"success": upgrade_successful}
