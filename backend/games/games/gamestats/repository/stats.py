import random

import time

from common.repositories import BaseRepository

from ..services.stats import GamesStatsService
from ..serializers import StatsSerializer


class GamesStatsRepository(BaseRepository):
    default_service = GamesStatsService()
    default_serializer_class = StatsSerializer

    _service: GamesStatsService

    def get(self) -> dict:
        data = self._service.get()

        shifted_online = data.online + random.randint(-2, 2)

        data.online = min(max(int(data / 200), shifted_online), data.users / 3.33)

        self._service.update_online(updated=data.online)

        return StatsSerializer(instance=data).data
