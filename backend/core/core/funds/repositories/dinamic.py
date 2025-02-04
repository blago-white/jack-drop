from common.repositories.base import BaseRepository
from ..serializers import UpdateDinamicSiteProfitSerializer
from ..services.dinamic import DinamicFundsService
from ..services.cases import CasesProfitService


class DinamicFundsRepository(BaseRepository):
    default_service = DinamicFundsService()
    default_cases_profit_service = CasesProfitService()
    default_serializer_class = UpdateDinamicSiteProfitSerializer

    _service: DinamicFundsService

    def __init__(self, *args, cases_profit_service: CasesProfitService = None, **kwargs):
        self._cases_profit_service = cases_profit_service or self.default_cases_profit_service

        super().__init__(*args, **kwargs)

    def increase(self, data: dict) -> dict:
        serialized = self._get_serialized(request_data=data)

        self._service.update(
            delta_funds=abs(serialized.validated_data.get("delta_amount"))
        )

        if serialized.data.get("for_cases"):
            self._cases_profit_service.update(
                delta_funds=abs(serialized.validated_data.get("delta_amount"))
            )

        return {"ok": True}

    def decrease(self, data: dict) -> dict:
        serialized = self._get_serialized(request_data=data)

        self._service.update(
            delta_funds=-abs(serialized.validated_data.get("delta_amount"))
        )

        if serialized.data.get("for_cases"):
            self._cases_profit_service.update(
                delta_funds=-abs(serialized.validated_data.get("delta_amount"))
            )

        return {"ok": True}

    def get(self) -> dict:
        amount = self._service.get()

        cases_amount = self._cases_profit_service.get()

        print(f"AMOUNT SENDED: {amount} : {cases_amount}")
        return {"amount": amount, "amount_cases": cases_amount}

    def _get_serialized(self, request_data: dict) -> UpdateDinamicSiteProfitSerializer:
        serialized: UpdateDinamicSiteProfitSerializer = self._serializer_class(
            data=request_data
        )

        serialized.is_valid(raise_exception=True)

        print("DINAMIC", serialized.data.get("delta_amount"))

        return serialized
