from common.views.django import BaseListView

from ..services.categories import CaseCategoriesService


class CasesCategoriesView(BaseListView):
    _service = CaseCategoriesService()
    template_name = "main.html"
    context_object_name = "cases"

    def get_queryset(self):
        print(self._service.get_cases_by_categories())
        return self._service.get_cases_by_categories()
