from common.repositories.default import DefaultRepository

from ..services.cases import CasesService
from ..serializers.case import CaseSerializer


class CasesRepository(DefaultRepository):
    _service = CasesService()
    _serializer = CaseSerializer
