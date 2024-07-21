import aiohttp

from .config import ConfigModelService


class WithdrawResultService:
    _fail_callback_url: str
    _callback_url: str

    def __init__(
            self,
            config_service: ConfigModelService = ConfigModelService()
    ):
        self._callback_url = config_service.get_withdraw_callback_url()

    async def send_success_callback(self) -> bool:
        result = await self._send_callback(
            data={"success": True},
        )

        return result

    async def send_result(self, error_items_ids: list[int],
                          success_items_ids: list[int]
                          ) -> bool:
        result = await self._send_callback(
            data={"error_items_ids": error_items_ids,
                  "succes_items_ids": success_items_ids},
        )

        return result

    async def _send_callback(self, data: dict) -> bool:
        if not self._callback_url:
            return True

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=self._callback_url,
                data=data
            ) as response:
                return await response.ok
