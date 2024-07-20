import random

from common.services.base import BaseModelService

from .transfer import MinesGameRequest, MinesGameResult, FundsDifference
from ..models import MinesGame


class MinesService:
    def next_step(self, game_request: MinesGameRequest) -> MinesGameResult:
        rate_per_win_item = game_request.count_mines / 25

        depo_win_rate = self.get_win_rate(
            step=game_request.step
        ) * max(1+rate_per_win_item-0.16, 1)

        win_rate = rate_per_win_item * 3

        if game_request.user_advantage > 0:
            if game_request.step == 1 and random.randint(0, 100) < 50:
                return self._get_win_result(
                    game_request=game_request,
                    win_rate=depo_win_rate
                )

            return self._get_loss_result(
                game_request=game_request,
            )

        random_num = random.randint(0, 100) / 100

        win = True if random_num < ((1 - rate_per_win_item) / 3) else False

        if win:
            if (game_request.site_active_funds > (
                    game_request.user_deposit * win_rate
            )):
                return self._get_win_result(
                    game_request=game_request,
                    win_rate=win_rate
                )

            else:
                return self._get_loss_result(
                    game_request=game_request,
                )

        return self._get_loss_result(
            game_request=game_request,
        )

    @staticmethod
    def _get_loss_result(game_request: MinesGameRequest) -> MinesGameResult:
        return MinesGameResult(
            is_win=False,
            funds_diffirence=FundsDifference(
                user_funds_diff=-game_request.user_deposit,
                site_funds_diff=(
                    game_request.user_deposit
                )
            ),
        )

    @staticmethod
    def _get_win_result(
            game_request: MinesGameRequest,
            win_rate: float) -> MinesGameResult:
        user_win_amount = game_request.user_deposit * win_rate

        return MinesGameResult(
            is_win=True,
            funds_diffirence=FundsDifference(
                user_funds_diff=user_win_amount,
                site_funds_diff=-user_win_amount
            )
        )

    @staticmethod
    def get_win_rate(step) -> float:
        if step == 1:
            return 0.01

        return 0.01 * min(max((step**2 / 10)+3, 1), 72)


class MinesModelService(BaseModelService):
    default_model = MinesGame

    def save(
            self, user_id: int,
            count_mines: int,
            mines_game_result: MinesGameRequest) -> MinesGame:
        return self._model.objects.create(
            user_id=user_id,
            count_mines=count_mines,
            is_win=mines_game_result.is_win,
            loss_step=mines_game_result.loss_step
        )
