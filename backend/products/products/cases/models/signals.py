from django.db.models.signals import post_save, post_delete

from cases.services.chances import (CaseItemsChancesService,
                                    BaseCaseItemsChancesService)
from .items import CaseItem


def update_case_items_rates(
        *args,
        instance: CaseItem,
        case_items_service: BaseCaseItemsChancesService = None,
        **kwargs):
    print("UPDATE CHANCES")

    manager = case_items_service or CaseItemsChancesService()

    manager.update_chanses(case=instance.case)


post_save.connect(update_case_items_rates, sender=CaseItem)
post_delete.connect(update_case_items_rates, sender=CaseItem)
