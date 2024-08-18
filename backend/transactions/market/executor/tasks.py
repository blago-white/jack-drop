import math
from asgiref.sync import async_to_sync, sync_to_async
from celery import shared_task

from schedule.models import ScheduledItem
from schedule.services.schedule import ScheduleModelService
from .services.apikey import ApiKeyService
from .services.callback import WithdrawResultService
from .services.withdraw import ItemWithdrawService
from .services.balance import ApiBotBalanceService


async def _apply_withdraw(items: list[ScheduledItem], apikey: str) -> bool:
    await _update_balance(items=items)

    callback_service = await sync_to_async(WithdrawResultService)()

    ok, error_items_ids = await ItemWithdrawService(
        apikey=apikey
    ).bulk_withdraw(items=items)

    success_items_ids = set([i.inventory_item_id for i in items]).difference(
        set(error_items_ids)
    )

    await callback_service.send_result(
        error_items_ids=error_items_ids,
        success_items_ids=success_items_ids
    )


async def _update_balance(items: list[ScheduledItem]):
    balance_service = ApiBotBalanceService()

    current = await balance_service.get_current()

    summ = sum([i.price for i in items])

    await balance_service.replenish(amount=summ - int(current))


@shared_task(name="withdraw")
def withdraw():
    items = list(ScheduleModelService().pop_schedule())

    if items:
        async_to_sync(_apply_withdraw)(items, ApiKeyService().apikey)

        return items
