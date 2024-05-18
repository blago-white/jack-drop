from common.views.api import DefaultRetrieveCreateApiView
from ..repositories.drop import CaseItemDropRepository


class DropCaseItemApiView(DefaultRetrieveCreateApiView):
    repository = CaseItemDropRepository()
    pk_url_kwarg = "case_id"

    def retrieve(self, request, *args, **kwargs):
        dropped = self.repository.get(request=request,
                                      case_id=self.get_requested_pk())

        return self.get_201_response(data=dropped)
