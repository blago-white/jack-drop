from common.services.base import BaseModelService

from .transfer import CreateTransactionData, UpdateTransactionData
from ..models import Payment, PaymentStatus


class PaymentsService(BaseModelService):
    default_model = Payment

    def init(self, data: CreateTransactionData) -> Payment:
        self.clean_irrelevant(user_id=data.user_id)

        return self._model.objects.create(
            user_id=data.user_id,
            amount_local=data.amount_from,
            promocode=data.promocode
        )

    def clean_irrelevant(self, user_id: int):
        if existed := self._model.objects.filter(
            user_id=user_id,
            status=None
        ).values_list("payment_id", flat=True):
            self._model.objects.filter(payment_id__in=existed).update(
                status=PaymentStatus.FAILED
            )

        return existed

    def cancel(self, tid: int):
        item: Payment = self.get(tid=tid)

        item.status = PaymentStatus.FAILED

        item.save()

    def get(self, tid: int, status=None) -> Payment:
        qs = self._model.objects.filter(
            pk=tid,
        )

        if status:
            qs = qs.filter(status=status)

        return qs.first()

    def set_status(self, tid: int, status: PaymentStatus):
        transaction = self.get(tid)

        transaction.status = status

        transaction.save()

    def update_data(self, tid: int, data: UpdateTransactionData):
        transaction = self.get(tid=tid)

        for colname in data.__dict__:
            setattr(transaction, colname, getattr(data, colname))

        transaction.full_clean()
        transaction.save()

        return transaction
