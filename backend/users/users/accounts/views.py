from steamauth import auth, get_uid

from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.urls import reverse
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .repositories.users import PrivateUsersRepository


class SteamAuthView(RedirectView):
    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("https://jackdrop.online/")

        return auth(
            response_url="https://jackdrop.online" + reverse("login-callback"),
            use_ssl=False
        )


class SteamAuthProcessView(RedirectView):
    repository = PrivateUsersRepository()

    def get(self, request, *args, **kwargs):
        steam_uid = get_uid(results=request.GET)

        if steam_uid is None:
            return redirect(to="https://jackdrop.online/?loginfail=1")

        token = self.repository.get(
            steam_id=steam_uid
        )

        if not token:
            token = self.repository.create(
                steam_uid=steam_uid
            )

        response = HttpResponseRedirect(
            redirect_to="https://jackdrop.online/",
        )

        response.set_cookie('access', token.get("access"))
        response.set_cookie('refresh', token.get("refresh"))

        return response
