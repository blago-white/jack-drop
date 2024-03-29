from common.services.base import BaseModelService

from ..models.cases import Case


class CasesService(BaseModelService):
    _model = Case
