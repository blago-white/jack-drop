from rest_framework.request import Request

from common.mixins.api import ModelAPIViewMixin
from common.views.api import BaseListAPIView, BaseRetreiveAPIView

from ..repositories.cases import CasesRepository
from ..serializers.case import CaseSerializer
from ..mixins.cases import CaseAPIViewMixin


class CasesByCategoriesListAPIView(BaseListAPIView):
    _repository = CasesRepository()

    def list(self, request: Request, *args, **kwargs):
        return self.get_200_response(
            data=self._repository.get_all_by_categories(
                min_price=request.query_params.get("min"),
                max_price=request.query_params.get("max"),
                category=request.query_params.get("cat")
            )
        )


class PaidCasesListAPIView(CaseAPIViewMixin, BaseListAPIView):
    def list(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self._repository.get_paid()
        )


class CasesListAPIView(CaseAPIViewMixin, BaseListAPIView):
    pass


class CaseRetrieveAPIView(CaseAPIViewMixin, BaseRetreiveAPIView):
    pass
