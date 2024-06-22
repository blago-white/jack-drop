from celery import shared_task

from .services import refresh


@shared_task(name="refresh_prices")
def refresh_prices():
    refresh.refresh_prices()
