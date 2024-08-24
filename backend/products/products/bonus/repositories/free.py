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

    def add(self, request_data: dict) -> dict:
        data = self._serializer_class(data=request_data)

        data.is_valid(raise_exception=True)

        if not self._deposits_model_service.validate_deposit_id(
                deposit_id=data.data.get("deposit_id")
        ):
            raise ValidationError(
                detail="Deposit id used",
                code=403
            )

        free_case = self._service.get_for_deposit(
            amount=float(data.data.get("amount"))
        )

        self._bonus_buy_service.add_case(
            user_id=data.data.get("user_id"),
            case=free_case
        )

        print("OK TRUE")

        return {"ok": True, "case": self._case_serializer(
            instance=free_case
        ).data}
