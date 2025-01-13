from rest_framework.exceptions import ValidationError

from common.repositories.base import BaseRepository
from cases.services.cases import CaseService
from cases.serializers.case import CaseSerializer

from ..services.bonus import BonusBuyService
from ..services.free import FreeCasesService, FreeCasesDepositsService
from ..serializers import UserFreeCaseAddSerializer


class FreeCasesRepository(BaseRepository):
    default_deposits_model_service = FreeCasesDepositsService()
    default_bonus_buy_service = BonusBuyService()
    default_service = FreeCasesService()

    default_serializer_class = UserFreeCaseAddSerializer
    default_case_serializer = CaseSerializer

    _service: FreeCasesService

    def __init__(self, *args,
                 bonus_buy_service: BonusBuyService = None,
                 deposits_model_service: FreeCasesDepositsService = None,
                 case_serializer: CaseSerializer = None,
                 **kwargs):
        self._bonus_buy_service = bonus_buy_service or self.default_bonus_buy_service
        self._deposits_model_service = deposits_model_service or self.default_deposits_model_service
        self._case_serializer = case_serializer or self.default_case_serializer

        super().__init__(*args, **kwargs)

    def get_for_deposit(self, deposit: float) -> dict:
        free_case = self._service.get_for_deposit(amount=deposit)

        if not free_case:
            raise ValidationError(400)

        return self._case_serializer(
            instance=free_case
        ).data
