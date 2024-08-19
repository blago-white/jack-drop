from common.repositories.base import BaseRepository

from ..services.transactions import TransactionApiService
from ..services.config import ConfigService
from ..services.transfer import CreateTransactionData, ApiCredentals
from ..serializers import TransactionCreationSerializer


class CardPaymentsRepository(BaseRepository):
    default_serializer_class = TransactionCreationSerializer
    default_service = TransactionApiService

    _service: TransactionApiService

    def __init__(self, *args,
                 config_service: ConfigService = ConfigService(),
                 **kwargs):
        self._config_service = config_service

        super().__init__(*args, **kwargs)

        self._service = self.default_service(
            credentals=ApiCredentals(
                pub=self._config_service.get().public_apikey,
                private=self._config_service.get().private_apikey
            )
        )

    def create(self, request_data: dict):
        serialized: TransactionCreationSerializer = self._serializer_class(data=request_data)

        serialized.is_valid(raise_exception=True)

        ok, response = self._service.create(
            data=self._serialize_create_request(
                serialized=serialized
            )
        )

        if ok:
            return response

    def _serialize_create_request(self, serialized: dict):
        return CreateTransactionData(
            user_id=serialized.get("user_id"),
            amount_from=serialized.data.get("amount"),
            from_=serialized.data.get("payin"),
            to=self._config_service.get().bank_currency_code,
            recipient_address=self._config_service.get().recipient_addres
        )
