from common.repositories.base import BaseRepository

from games.services.result import GameResultService
from games.serializers.result import GameResultsSerializer


class GameResultsRepository(BaseRepository):
    default_service = GameResultService()
    default_serializer_class = GameResultsSerializer

    _service: GameResultService

    def get_for_user(self, user_id: int) -> dict:
        return self._serializer_class(instance=self._service.get_for_user(
            user_id=user_id
        ), many=True).data
