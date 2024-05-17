from rest_framework.generics import RetrieveAPIView

from common.mixins.api import DetailedApiViewMixin

from cases.repositories.case import CasesRepository


class GetCaseDataPrivateApiView(DetailedApiViewMixin, RetrieveAPIView):
    pk_url_kwarg = "case_id"
    repository = CasesRepository()

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get(case_id=self.get_requested_pk())
        )
