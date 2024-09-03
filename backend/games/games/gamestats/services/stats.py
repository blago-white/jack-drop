from common.services.base import BaseModelService

from ..models import Stats, StatsDelta, AVAILABLE_STATS


def increase_all(increase_frequency: int = 5) -> None:
    stats: Stats = Stats.objects.all().first()
    stats_delta: StatsDelta = StatsDelta.objects.all().first()

    for stat_name in AVAILABLE_STATS:
        current = getattr(stats, stat_name)

        increase_amount_per_h = getattr(stats_delta, stat_name)

        increase_amount = (increase_amount_per_h / 60 / 60) * increase_frequency

        current += increase_amount

    stats.save()


class GamesStatsService(BaseModelService):
    default_model = Stats

    def get(self) -> Stats:
        return self.default_model.objects.all().first()
