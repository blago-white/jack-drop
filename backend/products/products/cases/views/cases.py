from common.views.django import BaseListView

from ..services.cases import CasesService


class CasesView(BaseListView):
    _service = CasesService()
    template_name = "cases.html"
