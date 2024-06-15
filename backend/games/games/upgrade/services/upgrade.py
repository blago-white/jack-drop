import random

from common.services.api.states import FundsState
from common.services.base import BaseModelService
from .shift import ChanceShiftService
from .result import UpgradeResult
from ..models import Upgrade


class UpgradeService(BaseModelService):
    default_model = Upgrade
    _shift_service = ChanceShiftService()

    def __init__(self, *args, shift_service: ChanceShiftService = None, **kwargs):
        if shift_service:
            self._shift_service = shift_service

        super().__init__(*args, **kwargs)

    def make_upgrade(
            self,
            user_id: int,
            granted_amount: float | int,
            receive_amount: float | int,
            funds_state: FundsState) -> UpgradeResult:
        self._model.objects.create(
            user_id=user_id,
            granted=granted_amount,
            received=receive_amount
        )

        is_win = self._is_win(
            granted_amount=granted_amount,
            receive_amount=receive_amount,
            funds_state=funds_state
        )

        user_balance_diff = (
                receive_amount-granted_amount
        ) if is_win else (-granted_amount)

        return UpgradeResult(
            user_balance_diff=user_balance_diff,
            success=is_win,
            site_active_funds_per_hour_diff=(
                granted_amount if not is_win else -user_balance_diff
            )
        )

    def _is_win(
            self,
            granted_amount: float | int,
            receive_amount: float | int,
            funds_state: FundsState) -> bool:
        win_rate = (granted_amount / receive_amount) * 100

        win_rate -= self._shift_service.get()

        if funds_state.usr_advantage > 0:
            win_rate //= 3

        elif funds_state.usr_advantage < 0 and abs(
                funds_state.usr_advantage
        ) > receive_amount and win_rate < 45:
            win_rate *= 2

        if (
                receive_amount-granted_amount >
                funds_state.site_active_funds_per_hour
        ) or (funds_state.usr_advantage > receive_amount / 2):
            return False

        random_num = random.randint(0, 100)

        if random_num <= win_rate:
            return True

        return False
