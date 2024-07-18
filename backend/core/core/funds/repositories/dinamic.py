from common.repositories.base import BaseRepository

from ..services.dinamic import DinamicFundsService
from ..serializers import UpdateDinamicSiteProfitSerializer


class DinamicFundsRepository(BaseRepository):
    default_service = DinamicFundsService()
    default_serializer_class = UpdateDinamicSiteProfitSerializer

    _service: DinamicFundsService

    def increase(self, data: dict) -> dict:
        serialized = self._get_serialized(request_data=data)

        self._service.update(
            delta_funds=abs(serialized.validated_data.get("delta_amount"))
        )

        return {"ok": True}

    def decrease(self, data: dict) -> dict:
        serialized = self._get_serialized(request_data=data)

        self._service.update(
            delta_funds=-abs(serialized.validated_data.get("delta_amount"))
        )

        return {"ok": True}

    def get(self) -> dict:
        return {"amount": self._service.get()}

    def _get_serialized(self, request_data: dict) -> UpdateDinamicSiteProfitSerializer:
        serialized: UpdateDinamicSiteProfitSerializer = self._serializer_class(
            data=request_data
        )

        print("DINAMIC", request_data)

        serialized.is_valid(raise_exception=True)

        return serialized
