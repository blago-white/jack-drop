from common.repositories import BaseRepository

from ..services.lottery import LotteryWinsModelService
from ..services.transfer import LotteryPrize, LotteryResult
from ..serializers import LotteryResultsSerializer


class LotteryWinsRepository(BaseRepository):
    default_service = LotteryWinsModelService
    default_serializer_class = LotteryResultsSerializer

    def add_result(self, data: dict):
        serialized = self._serializer_class(data=data)

        serialized.is_valid(raise_exception=True)

        self._service.add(result=self._serialize_to_dataclass(
            serialized=serialized
        ))

        return {"ok": True}

    @classmethod
    def _serialize_to_dataclass(
            cls, serialized: LotteryResultsSerializer
    ) -> LotteryResult:
        return LotteryResult(prizes=[
            LotteryPrize(
                winner_id=prize.data.winner_id,
                prize_item_id=prize.data.prize_item_id
            ) for prize in serialized.data.prizes
        ])
