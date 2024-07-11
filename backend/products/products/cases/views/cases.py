from common.views.django import BaseListView

from ..services.cases import CaseService


class CasesView(BaseListView):
    _service = CaseService()
    template_name = "cases.html"


