from rest_framework.exceptions import ValidationError
from django.forms import model_to_dict

from common.repositories.base import BaseRepository
from cases.serializers.case import CaseSerializer

from ..services.bonus import BonusBuyService, UserBonusesService
from ..serializers import BonusBuyProfileSerializer, UserBonusesSerializer


class BonusBuyRepository(BaseRepository):
    default_service = BonusBuyService()
    default_serializer_class = BonusBuyProfileSerializer
    default_case_serializer_class = CaseSerializer

    _service: BonusBuyService

    def __init__(self, *args,
                 case_serializer: CaseSerializer = None,
                 **kwargs):
        self._case_serializer_class = case_serializer or self.default_case_serializer_class

        super().__init__(*args, **kwargs)

    def get(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_or_create(
                user_id=user_id
            )
        ).data | {
            "can_withdraw_case": self._service.can_withdraw(user_id=user_id)
        }

    def next_level(self, user_id: int) -> dict:
        try:
            case = self.get_case(user_id=user_id)
        except ValidationError:
            case = {}

        result = self._service.next_level(user_id=user_id)

        if not result:
            raise ValidationError("Not enought points!")

        return {"ok": result, "receive": case}

    def get_case(self, user_id: int):
        case = self._service.withdraw_case(user_id=user_id)

        if not case:
            raise ValidationError("Cannot get case")

        return self._case_serializer_class(instance=case).data

    def has_withdrawed_case(self, user_id: int, case_id: int) -> dict:
        has = self._service.has_withdrawed_case(
            user_id=user_id,
            case_id=case_id
        )

        return {"ok": has}

    def get_withdrawed_cases(self, user_id: int) -> list[int]:
        cases = self._service.get_withdrawed_cases(user_id=user_id)

        return [i.pk for i in cases]


class UserBonusesRepository(BaseRepository):
    default_service = UserBonusesService()
    default_serializer_class = UserBonusesSerializer

    _service: UserBonusesService

    def get_discount(self, user_id: int, case_id: int) -> dict:
        return {
            "discount": self._service.get_discount(
                user_id=user_id, case_id=case_id
            )
        }

    def get_all_discounts(self, user_id: int) -> dict[str, list[dict[int, int]]]:
        return {
            "discounts": list(self._service.get_all_discounts(user_id=user_id))
        }

    def get_all(self, user_id: int) -> dict:
        return self._serializer_class(
            instance=self._service.get_all(user_id=user_id),
            many=True
        ).data
