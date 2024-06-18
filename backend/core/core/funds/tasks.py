import time

from celery import shared_task
from .services.dinamic import DinamicFundsService
from .services.frozen import FrozenFundsService
from .services.percent import FreezeFundsService


@shared_task(name="update_funds")
def update_funds(request):
    dinamic_funds_service = DinamicFundsService()
    frozen_funds_service = FrozenFundsService()

    dinamic_funds = dinamic_funds_service.get()

    if dinamic_funds <= 1:
        return

    freeze_rate = FreezeFundsService().get()

    frozen_funds = dinamic_funds * (freeze_rate/100)

    print(f"Dinamic funds: {dinamic_funds} | Frozen: {frozen_funds}")
    print(f"Freeze rate: {freeze_rate / 100}")

    dinamic_funds_service.update(delta_funds=-frozen_funds)

    frozen_funds_service.update(delta_funds=frozen_funds)
