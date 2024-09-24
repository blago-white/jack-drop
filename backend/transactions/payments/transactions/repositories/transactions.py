from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..models import PaymentStatus
from ..services.transactions import TransactionApiService
from ..services.config import ConfigService
from ..services.transfer import CreateTransactionData, ApiCredentals, UpdateTransactionData
from ..serializers import TransactionCreationSerializer
from ..services.payments import PaymentsService


class PaymentsRepository(BaseRepository):
    default_serializer_class = TransactionCreationSerializer
    default_service = TransactionApiService
    default_payment_service = PaymentsService()

    _service: TransactionApiService

    def __init__(self, *args,
                 config_service: ConfigService = ConfigService(),
                 payment_service: PaymentsService = PaymentsService(),
                 **kwargs):
        self._config_service = config_service
        self._payment_service = payment_service or self.default_payment_service

        super().__init__(*args, **kwargs)

        config = self._config_service.get()

        if config:
            self._service = self.default_service(
                credentals=ApiCredentals(
                    apikey=config.apikey,
                    api_user_id=config.api_user_id
                )
            )
        else:
            self._service = None

    def create(self, data: dict):
        serialized: TransactionCreationSerializer = self._serializer_class(data=data)

        serialized.is_valid(raise_exception=True)

        serialized_dataclass = self._serialize_create_request(
            serialized=serialized
        )

        inited = self._payment_service.init(data=serialized_dataclass)

        ok, response = self._service.create(data=serialized_dataclass, tid=inited.pk)

        if ok:
            return {
                "payment_url": response.get("paymentUrl"),
            }

        print(response)

        self._payment_service.set_status(tid=inited.pk,
                                         status=PaymentStatus.FAILED)

        raise ValidationError(code=400,
                              detail=f"Erorr with creating transaction - "
                                     f"{str(response)}")

    def update_status(self, tid: int, status: str):
        self._payment_service.set_status(tid=tid, status=status)

    def update(self, tid: int, data: dict[str, str]):
        self._payment_service.update_data(
            tid=tid,
            data=UpdateTransactionData(
                status=data.get("status"),
                payment_method=data.get("transaction").get(
                    "selectedProvider"
                ).get("method"),
                currency=data.get("transaction").get("pricing").get(
                    "local"
                ).get("currency")
            )
        )

    def cancel(self, foreign_transaction_id: str):
        return self._service.cancel(foreign_transaction_id) or True

    def get_payeer_id(self, tid: int):
        return self._payment_service.get(
            tid=tid
        ).user_id

    def transaction_exists(self, tid: int, user_id: int):
        transaction = self._payment_service.get(
            tid=tid
        )

        return transaction and (transaction.user_id == user_id)

    def _close_irrelevant(self, user_id: int):
        irrelevant_ids = self._payment_service.clean_irrelevant(
            user_id=user_id
        )

        for irrelevant_id in irrelevant_ids:
            self.cancel(foreign_transaction_id=irrelevant_id)

    @staticmethod
    def _serialize_create_request(serialized: dict):
        return CreateTransactionData(
            user_id=serialized.data.get("user_id"),
            amount_from=serialized.data.get("amount"),
        )
