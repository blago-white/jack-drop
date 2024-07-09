from asgiref.sync import async_to_sync

from celery import shared_task

from schedule.models import ScheduledItem
from schedule.services.schedule import ScheduleModelService

from ..services.withdraw import ItemWithdrawService


async def _apply_withdraw(items: list[ScheduledItem]):
    tasks = ItemWithdrawService().bulk_withdraw(items=items)


@shared_task(name="withdraw")
def withdraw():
    items = list(ScheduleModelService().pop_schedule())

    async_to_sync(_apply_withdraw)(items)
