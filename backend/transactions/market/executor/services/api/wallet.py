import aiohttp

from django.conf import settings


class TronWalletApiService:
    async def pay(self, amount: float, to: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=settings.PAYMENT_API_SERVICE_METHODS.get(
                    "pay"
                ),
                data={"amount": amount, "to": to}
            ) as response:
                return await response.json()
