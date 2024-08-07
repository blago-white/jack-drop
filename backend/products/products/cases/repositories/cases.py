from common.repositories.default import DefaultRepository
from ..serializers.case import CaseSerializer
from ..serializers.categories import CasesByCategoriesSerializer
from ..services.cases import CaseService
from ..services.categories import CaseCategoriesService


class CasesRepository(DefaultRepository):
    _service = CaseService()
    _category_service = CaseCategoriesService()
    _case_category_serializer = CasesByCategoriesSerializer
    _serializer = CaseSerializer

    def get_paid(self):
        return self._serializer(
            instance=self._service.get_paid(),
            many=True
        ).data

    def get_all_by_categories(self, min_price: int = None,
                              max_price: int = None,
                              category: str = None) -> dict:
        if category is None:
            categories = self._category_service.get_all()
        else:
            categories = self._category_service.bulk_get_titles(
                titles=[category]
            )

        result = dict.fromkeys(categories.values_list("title", flat=True))

        for cat in categories:
            result[cat.title] = list(self._service.get_all_for_category(
                category=cat.title,
                min_price=min_price,
                max_price=max_price
            ))

        json_result = []

        for cat in categories:
            if not result[cat.title]:
                continue

            json_result.append(
                {"category": cat,
                 "cases": result[cat.title]}
            )

        return self._case_category_serializer(instance=json_result, many=True).data
