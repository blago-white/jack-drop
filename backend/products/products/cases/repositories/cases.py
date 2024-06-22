from common.repositories.default import DefaultRepository

from ..services.cases import CaseService
from ..serializers.case import CaseSerializer


class CasesRepository(DefaultRepository):
    _service = CaseService()
    _serializer = CaseSerializer
