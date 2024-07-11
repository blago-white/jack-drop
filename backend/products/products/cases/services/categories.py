from django.db.models import QuerySet

from ..models.category import CasesCategory

from common.services.default import DefaultModelService


class CaseCategoriesService(DefaultModelService):
    default_model = CasesCategory

    def get_cases_by_categories(self) -> list[QuerySet]:
        categories_qs = self._model.objects.all().select_related()

        return [category.case_set.all() for category in categories_qs]

    def bulk_get_titles(self, titles: list[str]) -> QuerySet:
        return self._model.objects.filter(title__in=titles)
