from common.services.base import BaseModelService

from .transfer import CreateTransactionData
from ..models import Payment, PaymentStatus


class PaymentsService(BaseModelService):
    default_model = Payment

    def init(self, data: CreateTransactionData) -> Payment:
        return self._model.objects.create(
            user_id=data.user_id,
            user_ip=data.user_ip,
            payin_amount=data.amount_from,
            payin_currency=data.currency
        )

    def complete(self, tid: int):
        item: Payment = self._get(tid=tid)

        item.status = PaymentStatus.SUCCESS

    def abort(self, tid: int):
        item: Payment = self._get(tid=tid)

        item.status = PaymentStatus.FAIL

    def _get(self, tid: int) -> Payment:
        return self._model.objects.filter(pk=tid).first()
