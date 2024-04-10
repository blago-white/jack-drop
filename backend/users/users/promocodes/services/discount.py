from common.services import BaseService

from accounts.models import Client


class DiscountService(BaseService):
    default_model = Client

    def get(self, user_id):
        return self._model.objects.get(pk=user_id).promocode
