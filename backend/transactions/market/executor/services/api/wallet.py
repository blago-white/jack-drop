import aiohttp

from django.conf import settings


class TronWalletApiService:
    routes = settings.PAYMENT_API_SERVICE_METHODS

    async def pay(self, amount: float, to: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self.routes.get(
                    "pay"
                ),
                data={"amount": amount, "to": to}
            ) as response:
                return await response.json()
