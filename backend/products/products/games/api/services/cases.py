from cases.repositories.case import CasesRepository

from common.repositories.base import BaseRepository


class CaseDropRepository(BaseRepository):
    default_cases_repository = CasesRepository
    default_case_items_repository = Case

    def get_data_for_drop(self, case_id: int) -> dict:
        pass
