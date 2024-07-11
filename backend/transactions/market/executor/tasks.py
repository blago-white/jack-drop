from asgiref.sync import async_to_sync
from celery import shared_task

from schedule.models import ScheduledItem
from schedule.services.schedule import ScheduleModelService
from .services.apikey import ApiKeyService
from .services.callback import WithdrawResultService
from .services.withdraw import ItemWithdrawService


async def _apply_withdraw(items: list[ScheduledItem]) -> bool:
    apikey = ApiKeyService().apikey
    callback_service = WithdrawResultService()

    ok, error_items = await ItemWithdrawService(
        apikey=apikey
    ).bulk_withdraw(items=items)

    if not ok:
        return await callback_service.send_fail_callback(
            items_ids=items
        )

    return await callback_service.send_success_callback()


@shared_task(name="withdraw")
def withdraw():
    items = list(ScheduleModelService().pop_schedule())

    async_to_sync(_apply_withdraw)(items)
