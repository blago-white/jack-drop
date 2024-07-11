import random

from common.services.base import BaseModelService

from .transfer import MinesGameRequest, MinesGameResult, FundsDifference
from ..models import MinesGame


class MinesService:
    def get_result(self, game_request: MinesGameRequest) -> MinesGameResult:
        rate_per_win_item = game_request.count_mines / 25

        win_rate = rate_per_win_item*3

        if game_request.user_advantage > 0:
            return self._get_loss_result(
                game_request=game_request,
                count_mines=game_request.count_mines
            )

        random_num = random.randint(0, 100) / 100

        win = True if random_num < ((1-rate_per_win_item)/3) else False

        if win:
            if (game_request.site_active_funds > (
                    game_request.user_deposit*win_rate
            )):
                return self._get_win_result(
                    game_request=game_request,
                    win_rate=win_rate
                )

            else:
                return self._get_loss_result(
                    game_request=game_request,
                    count_mines=game_request.count_mines,
                )

        return self._get_loss_result(
            game_request=game_request,
            count_mines=game_request.count_mines,
        )

    @staticmethod
    def _get_loss_result(game_request: MinesGameRequest,
                         count_mines: float) -> MinesGameResult:
        return MinesGameResult(
            is_win=False,
            funds_diffirence=FundsDifference(
                user_funds_diff=-game_request.user_deposit,
                site_funds_diff=(
                    game_request.user_deposit
                )
            ),
            loss_step=random.randint(0, 25 - count_mines)
        )

    @staticmethod
    def _get_win_result(game_request: MinesGameRequest,
                        win_rate: float) -> MinesGameResult:
        user_win_amount = game_request.user_deposit * win_rate

        return MinesGameResult(
            is_win=True,
            funds_diffirence=FundsDifference(
                user_funds_diff=user_win_amount,
                site_funds_diff=-user_win_amount
            )
        )


class MinesModelService(BaseModelService):
    default_model = MinesGame

    def save(self, user_id: int,
             count_mines: int,
             mines_game_result: MinesGameRequest) -> MinesGame:
        return self._model.objects.create(
            user_id=user_id,
            count_mines=count_mines,
            is_win=mines_game_result.is_win,
            loss_step=mines_game_result.loss_step
        )
