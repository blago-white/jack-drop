import aiohttp

from django.conf import settings

from common.services.base import BaseMarketApiService


class _BotReplenishService:
    async def replenish(self, amount: float):
        return


class ApiBotBalanceService(BaseMarketApiService):
    def __init__(
            self,
            *args,
            replenish_service: _BotReplenishService = _BotReplenishService(),
            **kwargs
    ):
        self._replenish_service = replenish_service

        super().__init__(*args, **kwargs)

    async def get_current(self) -> float:
        async with (aiohttp.ClientSession() as session):
            async with session.post(
                url=settings.BALANCE_MARKET_ENDPOINT_URL.format(
                    apikey=self._apikey,
                )
            ) as response:
                result = await response.json()

        if not result.get("success"):
            return 0.0

        return result.get("money")

    async def replenish(self, amount: float):
        return await self._replenish_service.replenish(amount=amount)
