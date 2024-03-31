from common.services.default import DefaultModelService

from ..models.cases import Case


class CasesService(DefaultModelService):
    _model = Case
