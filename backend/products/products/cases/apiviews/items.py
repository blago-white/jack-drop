from common.mixins.api import ModelAPIViewMixin
from common.views.api import BaseListAPIView

from cases.repositories.items import CasesItemsRepository
from cases.repositories.cases import CasesRepository
from cases.serializers.items import CaseWithItemsPrivateSerializer


class CaseItemsListAPIView(BaseListAPIView):
    serializer_class = CaseWithItemsPrivateSerializer
    _repository = CasesItemsRepository()
    _cases_repository = CasesRepository()

    def get_serialized_response(self):
        serialized = dict(
            case=self._get_related_case(),
            items=self._get_case_items()
        )

        return serialized

    def list(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.get_serialized_response()
        )

    def _get_related_case(self):
        return self._cases_repository.get(
            pk=self.kwargs.get("case_pk")
        )

    def _get_case_items(self):
        return self._repository.get_all_by_case(
            case_pk=self.kwargs.get("case_pk")
        )
