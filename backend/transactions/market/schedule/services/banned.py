from common.services.base import BaseModelService

from schedule.models import BannedOwner


class BannedOwnersModelService(BaseModelService):
    default_model = BannedOwner

    def is_banned(self, owner_id: int) -> bool:
        return not self._model.objects.filter(user_id=owner_id).exists()
