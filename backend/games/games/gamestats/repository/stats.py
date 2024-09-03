import time

from common.repositories import BaseRepository

from ..services.stats import GamesStatsService
from ..serializers import StatsSerializer


class GamesStatsRepository(BaseRepository):
    default_service = GamesStatsService()
    default_serializer_class = StatsSerializer

    _service: GamesStatsService

    def get(self) -> dict:
        return StatsSerializer(instance=self._service.get()).data
