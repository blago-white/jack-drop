from ..services.items import CaseItemsService
from ..serializers.items import CaseItemSerializer
from ..models.items import CaseItem


class CasesItemsRepository:
    _service = CaseItemsService(model=CaseItem)
    _serializer = CaseItemSerializer

    def get_all_by_case(self, case_pk: str):
        return self._serializer(
            self._service.get_case_items_for_case(case_pk=case_pk),
            many=True,
        ).data
