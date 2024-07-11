from items.serializers import ItemWithCaseItemSerializer
from ..models.items import CaseItem
from ..services.items import CaseItemsService


class CasesItemsRepository:
    _service = CaseItemsService(model=CaseItem)
    _serializer = ItemWithCaseItemSerializer

    def get_all_by_case(self, case_pk: str):
        case_items_qs = self._service.get_case_items_for_case(case_pk=case_pk)
        items_qs = self._service.get_related_items(
            case_items_queryset=case_items_qs
        )

        case_items_qs, items_qs = list(case_items_qs), list(items_qs)

        items_qs = {
            i.id: i for i in items_qs
        }

        case_items_ids = {
            i.item_id: {"id": i.id, "rate": i.rate}
            for i in case_items_qs
        }

        data = []

        for item_id in case_items_ids:
            data.append({
                "case_item_id": case_items_ids[item_id].get("id"),
                "rate": case_items_ids[item_id].get("rate"),
                "id": items_qs[item_id].id,
                "market_link": items_qs[item_id].market_link,
                "title": items_qs[item_id].title,
                "image_path": items_qs[item_id].image_path,
                "price": items_qs[item_id].price
            })

        return data
