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
            payin_currency=data.mehtod
        )

    def complete(self, tid: int, amount: float):
        item: Payment = self.get(tid=tid, amount=amount, status=PaymentStatus.PROGRESS)

        item.status = PaymentStatus.SUCCESS

        item.save()

    def abort(self, tid: int, amount: float):
        item: Payment = self.get(tid=tid, amount=amount, status=PaymentStatus.PROGRESS)

        item.status = PaymentStatus.FAIL

        item.save()

    def get(self, tid: int, amount: float, status=None) -> Payment:
        qs = self._model.objects.filter(
            pk=tid,
            payin_amount=amount,
        )

        if status:
            qs = qs.filter(status=status)

        return qs.first()
