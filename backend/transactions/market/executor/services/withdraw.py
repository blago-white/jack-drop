import aiohttp
from django.conf import settings

from common.services.base import BaseModelService

from schedule.models import ScheduledItem


class ItemWithdrawService(BaseModelService):
    async def bulk_withdraw(self, items: list[ScheduledItem]) -> bool:
        pass

    async def withdraw(self, item: ScheduledItem) -> bool:
        async with aiohttp.ClientSession(
            base_url=settings.WITHDRAW_MARKET_ENDPOINT_URL.format(
                apikey="...",
                hashname=item.item_market_hash_name,
                price=10*10,
                trandelink=item.trade_link
            )
        ):
            pass
