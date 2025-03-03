import datetime

from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository
from common.services.transfer.products import FreeDepositCase

from ..models import PaymentStatus, PaymentCurrency, PaymentSystem
from ..serializers import (TransactionCreationSerializer,
                           SkinifyTransactionCreationSerializer)
from ..services.config import ConfigService
from ..services.payments import PaymentsService
from ..services.transactions import NicepayTransactionApiService, \
    SkinifyTransactionApiService
from ..services.transfer import NicepayCreateTransactionData, ApiCredentals, \
    UpdateTransactionData, SkinifyCreateTransactionData


class PaymentsRepository(BaseRepository):
    default_serializer_class = TransactionCreationSerializer
    default_nicepay_service = NicepayTransactionApiService
    default_skinify_service = SkinifyTransactionApiService
    default_payment_service = PaymentsService()
    default_service = PaymentsService

    _NICEPAY_APIKEY: str = None

    _nicepay_service: NicepayTransactionApiService
    _skinify_service: SkinifyTransactionApiService

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
            self._nicepay_service = self.default_nicepay_service(
                credentals=ApiCredentals(
                    secret_key=config.secret_key,
                    merchant_id=config.merchant_id,
                    skinify_apikey=config.skinify_key
                )
            )
            self._skinify_service = self.default_skinify_service(
                credentals=ApiCredentals(
                    secret_key=config.secret_key,
                    merchant_id=config.merchant_id,
                    skinify_apikey=config.skinify_key
                )
            )

            self._NICEPAY_APIKEY = config.secret_key
            self._SKINIFY_APIKEY = config.skinify_key
        else:
            self._nicepay_service = None
            self._skinify_service = None

    @property
    def nicepay_secret_for_validation(self) -> str:
        if not self._NICEPAY_APIKEY:
            self._NICEPAY_APIKEY = self._config_service.get()

        return self._NICEPAY_APIKEY

    @property
    def skinify_secret_for_validation(self) -> str:
        if not self._SKINIFY_APIKEY:
            self._SKINIFY_APIKEY = self._config_service.get().skinify_key

        return self._SKINIFY_APIKEY

    def nicepay_create(
            self, data: dict, free_deposit_case: FreeDepositCase | None):
        serialized: TransactionCreationSerializer = self._serializer_class(
            data=data
        )

        serialized.is_valid(raise_exception=True)

        serialized_dataclass = self._serialize_nicepay_create_request(
            serialized=serialized,
            free_deposit_case=free_deposit_case
        )

        inited = self._payment_service.init(
            data=serialized_dataclass,
            payment_system=PaymentSystem.NICEPAY
        )

        ok, response = self._nicepay_service.create(
            data=serialized_dataclass,
            tid=inited.pk
        )

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

    def skinify_create(self, data: dict):
        print(data)

        serialized = SkinifyTransactionCreationSerializer(data=data)

        serialized.is_valid(raise_exception=True)

        serialized_dataclass = self._serialize_skinify_create_request(
            serialized=serialized
        )

        inited = self._payment_service.init(
            data=serialized_dataclass,
            payment_system=PaymentSystem.SKINIFY
        )

        ok, response = self._skinify_service.create(
            tid=inited.pk,
            data=serialized_dataclass,
        )

        if ok:
            return {"payment_url": response.get("url")}

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

    def nicepay_update(self, tid: int, data: dict[str, str]):
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

    def skinify_update(self, tid: int, data: dict[str, str]):
        if self._payment_service.get(tid=tid).status:
            raise ValidationError(f"Payment {tid} already completed, "
                                  f"cannot update!")

        status = (PaymentStatus.FAILED
                  if data.get("status") != "success" else
                  PaymentStatus.SUCCESS)

        self._payment_service.update_data(
            tid=tid,
            data=UpdateTransactionData(
                status=status,
                amount_local=data.get("amount"),
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
    def _serialize_skinify_create_request(
            serialized: dict,
    ):
        return SkinifyCreateTransactionData(
            user_id=serialized.data.get("id"),
            steam_id=serialized.data.get("steam_id"),
            trade_token=serialized.data.get("offer_trade_link")
        )

    @staticmethod
    def _serialize_nicepay_create_request(
            serialized: dict,
            free_deposit_case: FreeDepositCase | None
    ):
        return NicepayCreateTransactionData(
            user_id=serialized.data.get("user_id"),
            user_login=serialized.data.get("user_login"),
            amount_from=serialized.data.get("amount"),
            currency=PaymentCurrency.RUB,  # TODO: Remove default exp
            free_deposit_case=free_deposit_case,
            promocode=serialized.data.get("promocode")
        )
