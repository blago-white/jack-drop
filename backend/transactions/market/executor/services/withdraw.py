import asyncio
import math
import time
import aiohttp

from django.conf import settings

from common.services.base import BaseMarketApiService
from schedule.models import ScheduledItem
from .transfer import WithdrawResult
from ..models import Withdraw, WithdrawedItem


class ItemWithdrawService(BaseMarketApiService):
    _last_request_duration: float
    _max_RPS: int = 5
    _withdraw_model = Withdraw
    _withdraw_item_model = WithdrawedItem

    async def bulk_withdraw(
            self, items: list[ScheduledItem]
    ) -> tuple[bool, list[int]]:

        results = []
        request_min_duration = round((10 * 3) / 5, 3) + 20

        for item in items:
            results.append(await self.withdraw(item=item))

            if self._last_request_duration < request_min_duration:
                await asyncio.sleep(
                    request_min_duration - self._last_request_duration
                )

        success, fail_ids = all([i.success for i in results]), [
            i.inventory_item_id for i in results if not i.success
        ]

        self._commit_withdraw(items=items, success=success)

        return success, fail_ids

    async def withdraw(self, item: ScheduledItem) -> WithdrawResult:
        start = time.time()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=settings.WITHDRAW_MARKET_ENDPOINT_URL.format(
                        apikey=self._apikey,
                        hashname=item.item_market_hash_name,
                        price=10 * 10,
                        trandelink=item.trade_link
                    )
            ) as response:
                result = await response.json()

        self._last_request_duration = (time.time() - start) * 1000

        return WithdrawResult(
            success=result.get("success"),
            inventory_item_id=item.inventory_item_id,
            owner_trade_link=item.trade_link
        )

    def _commit_withdraw(
            self, items: list[WithdrawedItem],
            success: bool) -> Withdraw:
        withdraw = self._withdraw_model(
            success=success,
            items=[self._withdraw_item_model(
                market_link=item.market_link,
                owner_trade_link=item.owner_trade_link,
                success=item.success
            ) for item in items]
        )

        withdraw.save()

        return withdraw
