import random
from django.core.exceptions import ValidationError

from common.services.base import BaseModelService
from .transfer import MinesGameNextStepRequest, MinesGameStepResult, FundsDifference, MinesGameInitParams
from ..models import MinesGame


class MinesService:
    win_rate_by_mines: float
    win_amount: float

    def next_step(self, game_request: MinesGameNextStepRequest) -> MinesGameStepResult:
        self._calc_win_rate(count_mines=game_request.count_mines)
        self._calc_win_amount(game_request=game_request)

        if game_request.user_advantage <= 0:
            return self._get_step_result(additional_rate_factor=1,
                                         game_request=game_request)

        else:
            if game_request.user_advantage > self.win_amount * 2:
                return self._get_step_result(additional_rate_factor=1 / 3,
                                             game_request=game_request)
            else:
                return self._get_step_result(additional_rate_factor=0.8,
                                             game_request=game_request)

    def _calc_win_rate(self, count_mines: int):
        self.win_rate_by_mines = (24 - count_mines) / 24

    def _calc_win_amount(self, game_request: MinesGameNextStepRequest) -> float:
        if game_request.count_mines < 8:
            factor = 1.02

        elif game_request.count_mines < 12:
            factor = 1.04

        elif game_request.count_mines < 20:
            factor = 1.08

        else:
            factor = 1.1

        self.win_amount = factor * game_request.user_current_ammount

    def _get_step_result(self, additional_rate_factor: float,
                         game_request: MinesGameNextStepRequest) -> MinesGameStepResult:
        win = (random.randint(1, 100) <
               (self.win_rate_by_mines *
               additional_rate_factor * 100))

        if win and (game_request.site_active_funds < (
                self.win_amount - game_request.user_deposit
        ) + 100):
            return MinesGameStepResult(
                is_win=False,
                funds_diffirence=FundsDifference(
                    user_funds_diff=0,
                    site_funds_diff=self.win_amount
                )
            )

        return MinesGameStepResult(
            is_win=win,
            funds_diffirence=FundsDifference(
                user_funds_diff=0 if not win else (self.win_amount - game_request.user_deposit),
                site_funds_diff=-(self.win_amount - game_request.user_deposit) if win else game_request.user_deposit
            )
        )


class MinesModelService(BaseModelService):
    default_model = MinesGame

    def get_active(self, user_id: int, raise_exception: bool = False) -> MinesGame:
        active = self._model.objects.all().filter(
            user_id=user_id,
            commited=False
        )

        if not active.exists():
            if raise_exception:
                raise ValidationError("Game not found!")
            return

        return active.first()

    def init(self, data: MinesGameInitParams) -> MinesGame:
        if active := self.get_active(user_id=MinesGameInitParams.user_id):
            return False, active

        return True, self._model.objects.create(
            user_id=data.user_id,
            count_mines=data.count_mines,
            deposit=data.deposit,
        )

    def next_win_step(self, user_id: int, new_game_amount: float, step: int):
        active = self.get_active(user_id=user_id)

        active.game_amount = new_game_amount
        active.step = step

        active.save()

        return active

    def commit(
            self, user_id: int,
            mines_game_result: MinesGameNextStepRequest = None
    ) -> MinesGame:
        active = self.get_active(user_id=user_id,
                                 raise_exception=True)

        if mines_game_result:
            active.step = mines_game_result.step
            active.is_win = mines_game_result.is_win
            active.game_amount = mines_game_result.user_current_ammount

        active.commited = True

        active.save()

        return active
