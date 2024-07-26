from django.core.exceptions import ValidationError
from steam_web_api import Steam

from ..models.api import SteamApiKey


class SteamAccountsService:
    _steam_service: Steam

    _apikey_model = SteamApiKey

    def __init__(self, apikey: str = None):
        if apikey:
            _apikey = apikey

        else:
            _apikey = self._apikey_model.objects.all().first()

        if not _apikey:
            raise ValidationError("Add steam api key!")

        self._steam_service = Steam(key=_apikey)

    def get_username(self, steam_id: str | int) -> str:
        return self._steam_service.users.get_user_details(
            steam_id=steam_id
        ).get("player").get("personaname")
