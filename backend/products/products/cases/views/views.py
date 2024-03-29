from rest_framework.generics import ListAPIView

from common.mixins.api import ModelAPIViewMixin
from common.views.api import BaseListAPIView

from cases.repositories.cases import CasesRepository
from cases.serializers.case import CaseSerializer


class CasesListAPIView(ModelAPIViewMixin, BaseListAPIView):
    serializer_class = CaseSerializer
    _repository = CasesRepository()
