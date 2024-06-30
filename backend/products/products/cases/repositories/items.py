from items.serializers import ItemWithCaseItemSerializer

from ..services.items import CaseItemsService
from ..models.items import CaseItem


class CasesItemsRepository:
    _service = CaseItemsService(model=CaseItem)
    _serializer = ItemWithCaseItemSerializer

    def get_all_by_case(self, case_pk: str):
        case_items_qs = self._service.get_case_items_for_case(case_pk=case_pk)
        items_qs = self._service.get_related_items(
            case_items_queryset=case_items_qs
        )

        case_items_qs, items_qs = list(case_items_qs), list(items_qs)

        case_items_ids = {
            i.item_id: i.id
            for i in case_items_qs
        }

        data = []

        for item in items_qs:
            data.append({
                "case_item_id": case_items_ids[item.id],
                "id": item.id,
                "market_link": item.market_link,
                "title": item.title,
                "image_path": item.image_path,
                "price": item.price
            })

        return data
