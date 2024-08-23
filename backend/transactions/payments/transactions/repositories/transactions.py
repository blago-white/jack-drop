from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository

from ..models import PaymentStatus
from ..services.transactions import TransactionApiService
from ..services.config import ConfigService
from ..services.transfer import CreateTransactionData, ApiCredentals
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

        inited = self._payment_service.init(data=serialized_dataclass)

        method = self._service.create_card \
            if serialized_dataclass.mehtod == "R" \
            else self._service.create_crypto

        ok, response = method(data=serialized_dataclass, tid=inited.pk)

        if ok:
            return {
                "form_url": response.get("data").get("form_url"),
            }

        self._payment_service.abort(tid=inited.pk, amount=inited.payin_amount)

        raise ValidationError(code=400,
                              detail="Erorr with creating transaction")

    def close(self, callback_data: dict):
        tid = callback_data.get("merchant_id")

        success = callback_data.get("status") in (
            "successed", "accepted_successed", "repeated_accepted_successed"
        )

        amount = callback_data.get("old_fiat_amount")

        if not self._payment_service.get(
            tid=tid, amount=amount, status=PaymentStatus.PROGRESS
        ):
            return {"aborted": True, "amount": amount, "tid": tid}

        closing_method = self._payment_service.abort

        if success:
            closing_method = self._payment_service.complete

        closing_method(tid=tid, amount=amount)

        return {"aborted": not success, "amount": amount, "tid": tid}

    def get_payeer_id(self, tid: int, amount: float):
        return self._payment_service.get(
            tid=tid, amount=amount
        ).user_id

    def transaction_exists(self, tid: int, amount: float, user_id: int):
        transaction = self._payment_service.get(
            tid=tid, amount=amount
        )

        return transaction and (transaction.user_id == user_id)

    @staticmethod
    def _serialize_create_request(serialized: dict):
        return CreateTransactionData(
            user_ip=serialized.data.get("user_ip"),
            user_id=serialized.data.get("user_id"),
            username=serialized.data.get("username"),
            amount_from=serialized.data.get("amount"),
            mehtod=serialized.data.get("pay_method"),
        )
