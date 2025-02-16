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
            _apikey = self._apikey_model.objects.all().first().apikey

        if _apikey:
            self._steam_service = Steam(key=_apikey)

    def get_username(self, steam_id: str | int) -> str:
        return self._get_user(steam_id=steam_id).get("personaname")

    def get_avatar(self, steam_id: str | int) -> str:
        avatar_url = self._get_user(steam_id=steam_id).get("avatarfull")

        if "_full" not in avatar_url:
            avatar_url = avatar_url[:-4]+"_full.jpg"

        return avatar_url

    def _get_user(self, steam_id: str | int) -> dict:
        return self._steam_service.users.get_user_details(
            steam_id=steam_id
        ).get("player")
