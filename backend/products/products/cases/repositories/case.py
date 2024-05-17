from common.repositories.base import BaseRepository

from cases.services.cases import CaseService
from cases.serializers.case import CaseDetailedDataPrivateSerializer


class CasesRepository(BaseRepository):
    default_service = CaseService()
    default_serializer_class = CaseDetailedDataPrivateSerializer

    _service: CaseService

    def get(self, case_id: int):
        case = self._service.get(case_id=case_id)

        return self._serializer_class(case).data
