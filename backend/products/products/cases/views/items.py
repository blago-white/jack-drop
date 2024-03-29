from common.mixins.api import ModelAPIViewMixin
from common.views.api import BaseListAPIView

from cases.repositories.items import CasesItemsRepository
from cases.serializers.items import CaseItemSerializer


class CaseItemsListAPIView(ModelAPIViewMixin, BaseListAPIView):
    serializer_class = CaseItemSerializer
    _repository = CasesItemsRepository()

    def list(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self._repository.get_all_by_case(
                case_pk=kwargs.get("case_pk")
            ))
