from rest_framework.generics import CreateAPIView

from common.views.api import CreateApiViewMixin
from ..repositories.drop import CaseItemDropRepository


class DropCaseItemApiView(CreateApiViewMixin, CreateAPIView):
    repository = CaseItemDropRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        dropped = self.repository.drop_item(request=request)

        return self.get_201_response(data=dropped)
