from celery import shared_task

from .services.stats import increase_all


@shared_task(name="increase_stats")
def increase_stats(freq: int = 5):
    increase_all(increase_frequency=freq)
