from rest_framework.generics import CreateAPIView

from common.mixins.api.create import CreateApiViewMixin
from ..repositories.upgrade import UpgradeRepository


class UpgradeApiView(CreateApiViewMixin, CreateAPIView):
    repository = UpgradeRepository()

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            self.repository.upgrade(request=request)
        )
