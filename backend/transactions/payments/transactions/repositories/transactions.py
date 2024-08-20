from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..services.transactions import TransactionApiService
from ..services.config import ConfigService
from ..services.transfer import CreateTransactionData, ApiCredentals
from ..serializers import TransactionCreationSerializer
from ..services.payments import PaymentsService


class CardPaymentsRepository(BaseRepository):
    default_serializer_class = TransactionCreationSerializer
    default_service = TransactionApiService
    default_payment_service = PaymentsService()

    _service: TransactionApiService

    def __init__(self, *args,
                 config_service: ConfigService = ConfigService(),
                 **kwargs):
        self._config_service = config_service

        super().__init__(*args, **kwargs)

        self._service = self.default_service(
            credentals=ApiCredentals(
                apikey=self._config_service.get().apikey,
                api_user_id=self._config_service.get().api_user_id
            )
        )

    def create(self, data: dict):
        serialized: TransactionCreationSerializer = self._serializer_class(data=data)

        serialized.is_valid(raise_exception=True)

        serialized_dataclass = self._serialize_create_request(
            serialized=serialized
        )

        method = self._service.create_card \
            if serialized_dataclass.mehtod == "R" \
            else self._service.create_crypto

        ok, response = method(data=serialized_dataclass)

        if ok:
            self.default_payment_service.init(data=None)

            return {
                "form_url": data.get("data").get("form_url"),
            }

        raise ValidationError(code=400,
                              detail="Erorr with creating transaction")

    @staticmethod
    def _serialize_create_request(serialized: dict):
        return CreateTransactionData(
            user_ip=serialized.get("user_ip"),
            user_id=serialized.get("user_id"),
            username=serialized.get("username"),
            amount_from=serialized.data.get("amount"),
            mehtod=serialized.data.get("pay_method"),
        )
