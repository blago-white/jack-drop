import asyncio

import aiohttp
from django.conf import settings

from common.services.base import BaseMarketApiService
from schedule.models import ScheduledItem
from .transfer import WithdrawResult


class ItemWithdrawService(BaseMarketApiService):
    async def bulk_withdraw(
            self, items: list[ScheduledItem]
    ) -> tuple[bool, list[int]]:
        tasks = [self.withdraw(item=item) for item in items]

        results: list[WithdrawResult] = await asyncio.gather(*tasks)

        return (all([i.success for i in results]),
                [i.inventory_item_id for i in results if not i.success])

    async def withdraw(self, item: ScheduledItem) -> WithdrawResult:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=settings.WITHDRAW_MARKET_ENDPOINT_URL.format(
                    apikey=self._apikey,
                    hashname=item.item_market_hash_name,
                    price=10*10,
                    trandelink=item.trade_link
                )
            ) as response:
                result = await response.json()

        return WithdrawResult(
            success=result.get("success"),
            inventory_item_id=item.inventory_item_id
        )
