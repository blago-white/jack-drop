from .base import BaseRepository

from ..services.products import ProductsApiService
from ..services.serializers.products import ProductsDepositWebhookSerializer
from ..services.transfer.products import DepositCallback


class ProductsApiRepository(BaseRepository):
    default_service = ProductsApiService()
    default_serializer_class = ProductsDepositWebhookSerializer

    _service: ProductsApiService

    def send_deposit_callback(self, data: dict) -> dict:
        serialized: ProductsDepositWebhookSerializer = self._serializer_class(
            data=data
        )

        serialized.is_valid(raise_exception=True)

        response = self._service.send_deposit_callback(
            callback=self._convert_to_deposit_callback(
                data=data
            )
        )

        return response

    @staticmethod
    def _convert_to_deposit_callback(data: dict) -> DepositCallback:
        return DepositCallback(
            deposit_id=data.get("deposit_id"),
            deposit_original_amount=data.get("amount"),
            user_id=data.get("user_id")
        )
