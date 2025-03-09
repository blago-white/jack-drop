from common.services.base import BaseModelService

from .transfer import LotteryWinners
from ..models import LotteryEvent, LotteryParticipant


class LotteryModelService(BaseModelService):
    default_model = LotteryEvent

    def get_current(self) -> LotteryEvent | None:
        try:
            return self._model.objects.filter(is_active=True).first()
        except:
            return

    def participate(
            self, participant_id: int,
            to_main_lottery: bool = False
    ) -> bool:
        current_lottery = self.get_current()

        participant = LotteryParticipant(
            user_id=participant_id,
            lottery=current_lottery,
            to_main_lottery=to_main_lottery
        )

        participant.save()

        return True

    def get_participants(self, lottery: LotteryEvent) -> dict[str, list[int]]:
        participants: list[LotteryParticipant] = list(current.participants)

        return dict(
            main_lottery=[
                i.user_id for i in participants if i.to_main_lottery
            ],
            secondary_lottery=[
                i.user_id for i in participants if not i.to_main_lottery
            ]
        )

    def commit_results(self, lottery: LotteryEvent,
                       winners: LotteryWinners) -> bool:
        lottery.winner_main = winners.main_lottery_winner_id
        lottery.winner_secondary = winners.secondary_lottery_winner_id

        lottery.is_active = False

        lottery.save()

        return True
