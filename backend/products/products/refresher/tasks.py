from celery import shared_task

from cases.services.chances import (CaseItemsChancesService,
                                    BaseCaseItemsChancesService)

from .services import refresh


@shared_task(name="refresh_prices")
def refresh_prices():
    refresh.refresh_prices()

    chances_service = CaseItemsChancesService()

    chances_service.update_chances_for_all()
