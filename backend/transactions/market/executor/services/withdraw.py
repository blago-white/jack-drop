import asyncio
import math
import time
import aiohttp
import threading

from django.conf import settings

from common.services.base import BaseMarketApiService
from schedule.models import ScheduledItem
from .transfer import WithdrawResult
from ..models import Withdraw, WithdrawedItem


class ItemWithdrawService(BaseMarketApiService):
    _last_request_duration: float
    _max_RPS: int = 2
    _withdraw_model = Withdraw
    _withdraw_item_model = WithdrawedItem

    async def bulk_withdraw(
            self, items: list[ScheduledItem]
    ) -> tuple[bool, list[int]]:
        results, request_min_duration = [], 1000/(self._max_RPS-1)

        for item in items:
            results.append(await self.withdraw(item=item))

            if self._last_request_duration < request_min_duration:
                await asyncio.sleep(
                    (request_min_duration - self._last_request_duration)/1000
                )


        print(f"RESULTS LIST: {results}")

        success, fail_ids = all([i.success for i in results]), [
            i.inventory_item_id for i in results if not i.success
        ]

        commit = threading.Thread(target=self._commit_withdraw,kwargs={"items": items, "success": [r.inventory_item_id for r in results if r.success], "failed_items_ids": fail_ids})
                
        commit.start()
                        
        commit.join()

        return success, fail_ids

    async def withdraw(self, item: ScheduledItem) -> WithdrawResult:
        start = time.time()

        class_id, instance_id = self.get_class_instance_id(
            market_link=item.item_market_link
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=settings.WITHDRAW_MARKET_ENDPOINT_URL.format(
                        apikey=self._apikey,
                        classid=class_id,
                        instanceid=instance_id,
                        price=item.price*100,
                        trandelink=item.trade_link.replace("https://steamcommunity.com/tradeoffer/new/?partner=", "")
                    )
            ) as response:
                result = await response.json()

        print("WITHDRAW RESULT", result)

        self._last_request_duration = (time.time() - start) * 1000

        return WithdrawResult(
            success=result.get("result") == "ok",
            inventory_item_id=item.inventory_item_id,
            owner_trade_link=item.item_market_link,
        )

    def _commit_withdraw(
            self, items: list[WithdrawedItem],
            success: bool,
            failed_items_ids: list[int]) -> Withdraw:
        withdraw = self._withdraw_model(
            success=bool(success),
        )

        withdraw.save()

        saved_items = []

        for item in items:
            commited = self._withdraw_item_model(
                market_link=item.item_market_link,
                owner_trade_link=item.trade_link,
                owner_id=item.owner_id,
                success=(item.inventory_item_id in success)
            )

            commited.save()

            saved_items.append(commited)

        withdraw.items.add(*saved_items)

        return withdraw

    @staticmethod
    def get_class_instance_id(market_link: str) -> list[str, str]:
        return market_link.split("/item/")[-1].split("-")[:2]
