import random
from django.core.exceptions import ValidationError

from common.services.base import BaseModelService
from .transfer import MinesGameNextStepRequest, MinesGameStepResult, FundsDifference, MinesGameInitParams
from ..models import MinesGame


class MinesService:
    win_rate_by_mines: float
    win_amount: float

    def next_step(self, game_request: MinesGameNextStepRequest) -> MinesGameStepResult:
        self._calc_win_rate(step=game_request.step, count_mines=game_request.count_mines)
        self._calc_win_amount(game_request=game_request)

        print(f"MINES FUNDS IN SERVICE: {game_request.site_active_funds=}*.5 <= {self.win_amount}")
        print(f"MINES FUNDS IN SERVICE: {game_request.user_advantage=} <= 0")

        if game_request.site_active_funds <= self.win_amount*2:
            return self._get_step_result(additional_rate_factor=0,
                                         game_request=game_request)

        elif game_request.user_advantage <= 0:
            return self._get_step_result(additional_rate_factor=1,
                                         game_request=game_request)

        else:
            print(f"{game_request.user_advantage=} > {abs(self.win_amount * 2)}")
            if game_request.user_advantage > abs(self.win_amount * 2):
                return self._get_step_result(additional_rate_factor=0.825,
                                             game_request=game_request)
            else:
                return self._get_step_result(additional_rate_factor=0.925,
                                             game_request=game_request)

    def _calc_win_rate(self, step: int, count_mines: int):
        self.win_rate_by_mines = (25 - (count_mines+step)) / 24

    def _calc_win_amount(self, game_request: MinesGameNextStepRequest) -> float:
        count_mines = game_request.count_mines + (game_request.step-1)

        if count_mines < 3:
            factor = round(1.005 + (count_mines/100), 3)

        elif count_mines < 6:
            factor = round(1.1 + (count_mines - 3)/10, 3)

        elif count_mines < 9:
            factor = 1.27

        elif count_mines < 12:
            factor = round(1.4 + (count_mines - 10)/10, 3)

        elif count_mines < 20:
            factor = round(1.7 + (min(count_mines - 14, 2.5))/10, 3)

        else:
            factor = 1.9

        self.win_amount = factor * game_request.user_current_ammount
        print(f"WIN AMMO: {self.win_amount}")

        print(f"FACTOR: {factor} * {game_request.user_current_ammount}")
        return self.win_amount

    def _get_step_result(self, additional_rate_factor: float,
                         game_request: MinesGameNextStepRequest) -> MinesGameStepResult:
        win = (random.randint(1, 100) <
               (self.win_rate_by_mines *
               additional_rate_factor * 100))

        print(f"{self.win_rate_by_mines} * {additional_rate_factor} * 100")

        next_factor = self._get_next_step_win_rate(game_request=game_request)

        if win and (game_request.site_active_funds < (
                self.win_amount - game_request.user_deposit
        ) + 100):
            return MinesGameStepResult(
                is_win=False,
                funds_diffirence=FundsDifference(
                    user_funds_diff=-game_request.user_deposit,
                    site_funds_diff=game_request.user_deposit,
                ),
                next_win_factor=next_factor
            )

        return MinesGameStepResult(
            is_win=win,
            funds_diffirence=FundsDifference(
                user_funds_diff=-game_request.user_deposit if not win else (self.win_amount - game_request.user_current_ammount),
                site_funds_diff=-(self.win_amount - game_request.user_deposit) if win else game_request.user_deposit
            ),
            next_win_factor=next_factor
        )

    def _get_next_step_win_rate(self, game_request: MinesGameNextStepRequest) -> float:
        game_request.count_mines += 1
        game_request.step += 1

        real_win_amount = self.win_amount

        next_step_win_rate = (self._calc_win_amount(game_request=game_request) /
                              game_request.user_current_ammount)

        self.win_amount = real_win_amount

        game_request.count_mines -= 1
        game_request.step -= 1

        return next_step_win_rate


class MinesModelService(BaseModelService):
    default_model = MinesGame

    def get_active(self, user_id: int, raise_exception: bool = False) -> MinesGame:
        active = self._model.objects.all().filter(
            user_id=user_id,
            commited=False
        )

        print(user_id, active, self._model.objects.all().values())

        if not active.exists():
            if raise_exception:
                raise ValidationError("Game not found!")
            return

        return active.first()

    def init(self, data: MinesGameInitParams) -> MinesGame:
        if active := self.get_active(user_id=data.user_id):
            return False, active

        print(f"CREATED: {data.user_id} - {data.count_mines}")

        return True, self._model.objects.create(
            user_id=data.user_id,
            count_mines=data.count_mines,
            deposit=data.deposit,
            user_advantage=data.advantage,
            game_amount=data.deposit
        )

    def next_win_step(self, user_id: int, new_game_amount: float, step: int):
        active = self.get_active(user_id=user_id)

        active.game_amount = new_game_amount
        active.step = step

        active.save()

        return active

    def commit(
            self, user_id: int, is_win: bool
    ) -> MinesGame:
        active = self.get_active(user_id=user_id,
                                 raise_exception=True)

        active.is_win = is_win
        active.commited = True

        active.save()

        return active
