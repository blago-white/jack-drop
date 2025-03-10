from common.services.base import BaseModelService

from schedule.models import BannedOwner


class BannedOwnersModelService(BaseModelService):
    default_model = BannedOwner

    def is_banned(self, owner_id: int) -> bool:
        print(f"{owner_id=} {self._model.objects.filter(user_id=owner_id).exists()}")
        return bool(self._model.objects.filter(user_id=owner_id).exists())
