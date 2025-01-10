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
    #await _update_balance(items=items, apikey=apikey)

    print("START WITHDRAW")
    callback_service = await sync_to_async(WithdrawResultService)()

    ok, error_items_ids = await ItemWithdrawService(
        apikey=apikey
    ).bulk_withdraw(items=items)

    success_items_ids = set([i.inventory_item_id for i in items]).difference(
        set(error_items_ids)
    )

    print(f"WITHDRAW ITEMS {success_items_ids} : {error_items_ids}")

    await callback_service.send_result(
        error_items_ids=error_items_ids,
        success_items_ids=success_items_ids
    )

    return success_items_ids


async def _update_balance(items: list[ScheduledItem], apikey: str):
    balance_service = ApiBotBalanceService(apikey=apikey)

    current = await balance_service.get_current()

    summ = sum([i.price for i in items])

    if not summ or int(current) > summ:
        return

    await balance_service.replenish(amount=summ - int(current))


@shared_task(name="withdraw")
def withdraw():
    schedule_service = ScheduleModelService()
    items = schedule_service.get_schedule()

    if items:
        result = async_to_sync(_apply_withdraw)(items, ApiKeyService().apikey)

        schedule_service.bulk_delete_withdrawed(ids=result)

        return items

