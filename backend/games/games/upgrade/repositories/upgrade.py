from rest_framework.request import Request

from common.repositories import BaseRepository
from common.services.api.states import FundsState
from ..serializers import UpgradeRequestSerializer
from ..services.upgrade import UpgradeService


class UpgradeRepository(BaseRepository):
    default_service = UpgradeService()
    default_serializer_class = UpgradeRequestSerializer
    _service: UpgradeService
    _serializer_class: UpgradeRequestSerializer

    def upgrade(self, request: Request) -> dict:
        serialized: UpgradeRequestSerializer = self._serializer_class(
            data=request.data
        )

        serialized.is_valid(raise_exception=True)

        receive_amount = serialized.data.get("receive_funds")

        funds_state = FundsState(
            usr_advantage=float(
                serialized.data.get("user_funds").get("user_advantage")
            ),
            site_active_funds=float(
                serialized.data.get("site_funds").get(
                    "site_active_funds"
                )
            )
        )

        granted_amount = serialized.data.get("granted_funds")

        upgrade_result = self._service.make_upgrade(
            user_id=serialized.data.get("user_funds").get("id"),
            granted_amount=granted_amount,
            receive_amount=receive_amount,
            funds_state=funds_state
        )

        return {
            "user_balance_diff": upgrade_result.user_balance_diff,
            "site_funds": {
                "site_active_funds": upgrade_result.site_active_funds_diff
            },
            "success": upgrade_result.success
        }
