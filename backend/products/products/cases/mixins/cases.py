from ..repositories.cases import CasesRepository
from ..serializers.case import CaseSerializer


class CaseAPIViewMixin:
    _repository = CasesRepository()
    serializer_class = CaseSerializer
    pk_url_kwarg = "case_pk"


class CasesTemplateViewMixin:
    context_object_name = "cases"
