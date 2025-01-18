from celery import shared_task

from accounts.services.advantage import AdvantageService


@shared_task(name="inflate_advantage")
def inflate_advantage():
    advantage_service = AdvantageService()

    advantage_service.bulk_inflate_advantages()
