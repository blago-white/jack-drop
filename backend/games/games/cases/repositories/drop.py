from common.repositories import BaseRepository

from ..services.api.cases import CasesApiService


class CaseItemDropRepository(BaseRepository):
    _products_web_repository: CasesApiService

    def __init__(self, *args,
                 products_web_repository: CasesApiService = CasesApiService(),
                 **kwargs):
        self._products_web_repository = products_web_repository

        super().__init__(*args, **kwargs)

    def get(self, user_advantage: int, case_id: int):
        case_data = self._products_web_repository.get_info(
            case_id=case_id
        )

