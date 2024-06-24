from common.repositories.default import DefaultRepository

from ..services.categories import CaseCategoriesService
from ..services.cases import CaseService
from ..serializers.case import CaseSerializer
from ..serializers.categories import CasesByCategoriesSerializer


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

    def get_all_by_categories(self):
        categories = self._category_service.get_all()

        result = dict.fromkeys(categories.values_list("title", flat=True))

        for cat in categories:
            result[cat.title] = list(self._service.get_all_for_category(
                category=cat.title
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
