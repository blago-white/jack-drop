from django.contrib.auth.backends import BaseBackend

from rest_framework_simplejwt.models import TokenUser

from django.contrib.auth import get_user_model


class JWTAuthenticationWithoutPassword(BaseBackend):

    def authenticate(self, request, steam_uid=None):
        print(request, steam_uid, "___RRR")

        if steam_uid is None:
            steam_uid = request.data.get('steam_uid', '')
        try:
            return get_user_model().objects.get(steam_id=steam_uid)
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        print(user_id, "___RRR")

        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
