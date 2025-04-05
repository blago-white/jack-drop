from .model import LotteryModelService
from .random import LotteryRandomService
from .transfer import LotteryWinners
from ..models.lottery import LotteryEvent


class LotteryGameService:
    default_model_service = LotteryModelService()
    default_random_service = LotteryRandomService()

    def __init__(self, model_service: LotteryModelService = None,
                 random_service: LotteryRandomService = None):
        self._model_service = model_service or self.default_model_service
        self._random_service = random_service or self.default_random_service

    def implement_lottery(self) -> tuple[bool, LotteryEvent]:
        current: LotteryEvent | None = self._model_service.get_current()

        if not current:
            raise ValueError("Current lottery not found!")

        if current.is_dummy:
            self._model_service.deactivate_lottery(lottery=current)

            raise ValueError("Current lottery is dummy, without winners!")

        winners = self._get_winners(lottery=current)

        self._model_service.commit_results(
            lottery=current,
            winners=winners
        )

        return True, current

    def _get_winners(self, lottery: LotteryEvent) -> LotteryWinners:
        lottery_users = self._model_service.get_participants(
            lottery=lottery
        )

        main_lottery_winner = secondary_lottery_winner = None

        try:
            main_lottery_winner = self._random_service.get_winner(
                lottery_users.get("main_lottery")
            )
        except:
            pass

        try:
            secondary_lottery_winner = self._random_service.get_winner(
                lottery_users.get("secondary_lottery")
            )
        except:
            pass

        return LotteryWinners(
            main_lottery_winner_id=main_lottery_winner,
            secondary_lottery_winner_id=secondary_lottery_winner
        )
