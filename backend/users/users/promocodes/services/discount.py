from accounts.models import Client
from common.services import BaseService


class DiscountService(BaseService):
    default_model = Client

    def get(self, user_id):
        return self._model.objects.drop_item(pk=user_id).promocode
