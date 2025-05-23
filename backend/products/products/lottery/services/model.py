from common.services.base import BaseModelService

from .transfer import LotteryWinners
from ..models.lottery import LotteryEvent, LotteryParticipant


class LotteryModelService(BaseModelService):
    default_model = LotteryEvent

    def deactivate_lottery(self, lottery: LotteryEvent):
        lottery.is_active = False
        lottery.save()

    def get_current(self) -> LotteryEvent | None:
        try:
            return self._model.objects.filter(is_active=True).first()
        except:
            return

    def get_by_id(self, lottery_id: int) -> LotteryEvent | None:
        try:
            return self._model.objects.get(pk=lottery_id)
        except:
            return

    def has_participate(self, participant_id: int) -> tuple[bool, bool]:
        current = self.get_current()

        if not current:
            return False, False

        return (
            current.participants.filter(
                to_main_lottery=True,
                user_id=participant_id
            ).exists(),
            current.participants.filter(
                to_main_lottery=False,
                user_id=participant_id
            ).exists()
        )

    def participate(
            self, participant_id: int,
            to_main_lottery: bool = False,
            balance: float = 0
    ) -> bool:
        current_lottery = self.get_current()

        if to_main_lottery and (balance < current_lottery.deposit_amount_require):
            raise ValueError

        current_lottery.display_participants_count += 1

        current_lottery.save()

        participant = LotteryParticipant(
            user_id=participant_id,
            lottery=current_lottery,
            to_main_lottery=to_main_lottery
        )

        participant.save()

        return True

    def get_participants(self, lottery: LotteryEvent) -> dict[str, list[int]]:
        participants: list[LotteryParticipant] = list(lottery.participants.all())

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
