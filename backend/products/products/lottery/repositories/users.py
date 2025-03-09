from common.repositories.base import BaseRepository

from ..services.transfer import LotteryWinners
from ..services.api.users import UsersLotteryApiService
from .transfer import LotteryResult


class UsersLotteryResultsApiRepository(BaseRepository):
    default_service = UsersLotteryApiService()
    default_serializer_class = default_service.default_endpoint_serializer_class

    _service: UsersLotteryApiService

    def send_results(self, results: LotteryResult):
        serialized = self._serializer_class(
            data=results.as_json()
        )

        serialized.is_valid(raise_exception=True)

        self._service.send_results(serialized=serialized)

        return True
