import random

from common.services.base import BaseModelService
from common.states import FoundsState

from ..models import Upgrade
from .shift import ChanceShiftService


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
            founds_state: FoundsState) -> bool:
        self._model.objects.create(
            user_id=user_id,
            granted=granted_amount,
            received=receive_amount
        )

        return self._is_win(
            granted_amount=granted_amount,
            receive_amount=receive_amount,
            founds_state=founds_state
        )

    def _is_win(
            self,
            granted_amount: float | int,
            receive_amount: float | int,
            founds_state: FoundsState) -> bool:
        win_rate = (granted_amount / receive_amount) * 100

        win_rate -= self._shift_service.get()

        if founds_state.usr_advantage > 0:
            win_rate //= 3

        elif founds_state.usr_advantage < 0 and abs(
                founds_state.usr_advantage
        ) > receive_amount and win_rate < 45:
            win_rate *= 2

        if (receive_amount > (founds_state.site_active_hour_funds + -(
                founds_state.usr_advantage
        ))) or (founds_state.usr_advantage > receive_amount / 2):
            return False

        random_num = random.randint(0, 100)

        if random_num <= win_rate:
            return True

        return False
