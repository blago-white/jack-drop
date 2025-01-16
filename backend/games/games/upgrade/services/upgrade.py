import random

from common.services.api.states import FundsState
from common.services.base import BaseModelService
from .result import UpgradeResult
from .shift import ChanceShiftService
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
            site_funds_diff=(
                granted_amount if not is_win else -user_balance_diff
            )
        )

    def _is_win(
            self,
            granted_amount: float | int,
            receive_amount: float | int,
            funds_state: FundsState) -> bool:
        if granted_amount > receive_amount:
            return True

        win_rate = (granted_amount / receive_amount) * 100

        win_rate -= self._shift_service.get()

        if funds_state.usr_advantage > 0:
            if funds_state.usr_advantage > receive_amount - granted_amount:
                win_rate *= 0.5 if win_rate < 80 else (0.6 if win_rate < 90 else 0.7)
            else:
                win_rate *= 0.85

        # elif funds_state.usr_advantage < 0 and abs(
        #         funds_state.usr_advantage
        # ) > receive_amount and win_rate <= 90:
        #     win_rate *= 1.1

        if (receive_amount-granted_amount)*2 > funds_state.site_active_funds:
            return False

        random_num = random.randint(0, 100)

        if random_num <= win_rate:
            return True

        return False
