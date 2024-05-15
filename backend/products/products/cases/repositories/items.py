from ..services.items import CaseItemsService
from ..serializers.items import CaseItemPrivateSerializer
from ..models.items import CaseItem


class CasesItemsRepository:
    _service = CaseItemsService(model=CaseItem)
    _serializer = CaseItemPrivateSerializer

    def get_all_by_case(self, case_pk: str):
        return self._serializer(
            self._service.get_case_items_for_case(case_pk=case_pk),
            many=True,
        ).data
