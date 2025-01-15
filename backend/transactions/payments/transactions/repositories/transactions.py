import datetime

from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository
from common.services.transfer.products import FreeDepositCase

from ..models import PaymentStatus, PaymentCurrency
from ..serializers import TransactionCreationSerializer
from ..services.config import ConfigService
from ..services.payments import PaymentsService
from ..services.transactions import TransactionApiService
from ..services.transfer import CreateTransactionData, ApiCredentals, \
    UpdateTransactionData


class PaymentsRepository(BaseRepository):
    default_serializer_class = TransactionCreationSerializer
    default_service = TransactionApiService
    default_payment_service = PaymentsService()

    _SECRET_KEY: str = None

    _service: TransactionApiService

    def __init__(
            self, *args,
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
                    secret_key=config.secret_key,
                    merchant_id=config.merchant_id
                )
            )
            self._SECRET_KEY = config.secret_key
        else:
            self._service = None

    @property
    def secret_for_validation(self) -> str:
        if not self._SECRET_KEY:
            self._SECRET_KEY = self._config_service.get()

        return self._SECRET_KEY

    def create(self, data: dict, free_deposit_case: FreeDepositCase | None):
        serialized: TransactionCreationSerializer = self._serializer_class(
            data=data
        )

        serialized.is_valid(raise_exception=True)

        serialized_dataclass = self._serialize_create_request(
            serialized=serialized,
            free_deposit_case=free_deposit_case
        )

        inited = self._payment_service.init(data=serialized_dataclass)

        ok, response = self._service.create(data=serialized_dataclass,
                                            tid=inited.pk)

        if not ok:
            raise ValidationError("Cannot create payment [resp]")

        try:
            self._payment_service.update_data(
                tid=inited.pk,
                data=UpdateTransactionData(
                    expired_at=datetime.datetime.fromtimestamp(
                        int(response.get("expired"))
                    ),
                    currency=serialized_dataclass.currency,
                )
            )
        except:
            raise ValidationError("Cannot create payment [exp]!")

        if ok:
            return {"payment_url": response.get("link")}

        self._payment_service.set_status(
            tid=inited.pk,
            status=PaymentStatus.FAILED
        )

        raise ValidationError(
            detail=f"Erorr with creating transaction - {response}"
        )

    def get_promocode(self, tid: int) -> str:
        return self._payment_service.get(tid=tid).promocode

    def update_status(self, tid: int, status: str):
        self._payment_service.set_status(tid=tid, status=status)

    def update(self, tid: int, data: dict[str, str]):
        if self._payment_service.get(
            tid=tid
        ).status:
            raise ValidationError(f"Payment {tid} already completed, "
                                  f"cannot update!")

        status = (PaymentStatus.FAILED
                  if data.get("result") != "success" else
                  PaymentStatus.SUCCESS)

        self._payment_service.update_data(
            tid=tid,
            data=UpdateTransactionData(
                status=status,
                payment_method=data.get("method"),
                currency=data.get("amount_currency")
            )
        )

    def get_payeer_id(self, tid: int):
        return self._payment_service.get(tid=tid).user_id

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
    def _serialize_create_request(
            serialized: dict,
            free_deposit_case: FreeDepositCase | None
    ):
        return CreateTransactionData(
            user_id=serialized.data.get("user_id"),
            user_login=serialized.data.get("user_login"),
            amount_from=serialized.data.get("amount"),
            currency=PaymentCurrency.RUB,  # TODO: Remove default exp
            free_deposit_case=free_deposit_case,
            promocode=serialized.data.get("promocode")
        )
