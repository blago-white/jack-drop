from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository
from games.serializers.result import GameResultsSerializer
from games.services.result import GameResultService
from games.models import Games


class GameResultsRepository(BaseRepository):
    default_service = GameResultService()
    default_serializer_class = GameResultsSerializer

    _service: GameResultService

    def get_for_user(self, user_id: int, game: str) -> dict:
        if game not in Games.values:
            raise ValidationError("Not correct section!")

        return self._serializer_class(instance=self._service.get_for_user(
            user_id=user_id,
            game=game
        ), many=True).data
