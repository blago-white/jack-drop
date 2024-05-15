from common.mixins.api import ModelAPIViewMixin
from common.views.api import BaseListAPIView, BaseRetreiveAPIView

from ..repositories.cases import CasesRepository
from ..serializers.case import CaseSerializer
from ..mixins.cases import CaseAPIViewMixin


class CasesListAPIView(CaseAPIViewMixin, BaseListAPIView):
    pass


class CaseRetrieveAPIView(CaseAPIViewMixin, BaseRetreiveAPIView):
    pass
