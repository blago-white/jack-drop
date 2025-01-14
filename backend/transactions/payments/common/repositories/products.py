from .base import BaseRepository

from ..services.products import ProductsApiService
from ..services.serializers.products import ProductsDepositWebhookSerializer
from ..services.transfer.products import DepositCallback

from common.services.transfer.products import FreeDepositCase


class ProductsApiRepository(BaseRepository):
    default_service = ProductsApiService()
    default_serializer_class = ProductsDepositWebhookSerializer

    _service: ProductsApiService

    def send_deposit_callback(self, data: dict) -> bool:
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

    def get_free_case_for_deposit(self, deposit_amount: float) -> FreeDepositCase:
        try:
            case = self._service.get_deposit_free_case(
                deposit_amount=deposit_amount
            )
        except Exception:
            return

        if case:
            return self._serialize_free_deposit_case(
                case_data=case
            )

    @staticmethod
    def _serialize_free_deposit_case(case_data: dict[str, str]):
        return FreeDepositCase(
            case_title=case_data.get("title"),
            case_img=case_data.get("image_path")
        )

    @staticmethod
    def _convert_to_deposit_callback(data: dict) -> DepositCallback:
        return DepositCallback(
            deposit_id=data.get("deposit_id"),
            deposit_original_amount=data.get("amount"),
            user_id=data.get("user_id")
        )
