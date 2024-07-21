from common.services.base import BaseModelService

from ..models.models import ItemsSet


class ItemSetService(BaseModelService):
    default_model = ItemsSet

    def get_all(self):
        return self._model.objects.all()

    def get(self, set_id: int) -> ItemsSet:
        return self._model.objects.get(pk=set_id)
