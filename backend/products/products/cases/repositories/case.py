from cases.serializers.case import CaseSerializer
from cases.services.cases import CaseService
from common.repositories.base import BaseRepository


class CasesRepository(BaseRepository):
    default_service = CaseService()
    default_serializer_class = CaseSerializer

    _service: CaseService

    def get(self, case_id: int):
        case = self._service.get(case_id=case_id)

        return self._serializer_class(case).data
