from steamauth import auth, get_uid

from django.shortcuts import redirect
from django.views.generic import RedirectView
from django.urls import reverse
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .repositories.users import PrivateUsersRepository
from referrals.repositories.referral import ReferrRepository


class BaseReflinkProcessingView(RedirectView):
    _REFER_LINK_FIELD = "ref"

    @property
    def _ref_id(self):
        return self.request.GET.get(self._REFER_LINK_FIELD)


class SteamAuthView(BaseReflinkProcessingView):
    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("https://jackdrop.online/")

        return auth(
            response_url=f"https://jackdrop.online/{reverse('login-callback')}"
                         f"&{self._REFER_LINK_FIELD}={self._ref_id}",
            use_ssl=False
        )


class SteamAuthProcessView(BaseReflinkProcessingView):
    repository = PrivateUsersRepository()
    referrs_repository = ReferrRepository()

    def get(self, request, *args, **kwargs):
        steam_uid = get_uid(results=request.GET)

        if steam_uid is None:
            return redirect(to="https://jackdrop.online/?loginfail=1")

        token = self.repository.get(
            steam_id=steam_uid
        )

        if not token:
            used_id, token = self.repository.create(
                steam_uid=steam_uid
            )

            if self._ref_id:
                self.referrs_repository.add_referr(
                    user_id=used_id,
                    referr_link=self._ref_id
                )

        response = HttpResponseRedirect(
            redirect_to="https://jackdrop.online/",
        )

        response.set_cookie('access', token.get("access"))
        response.set_cookie('refresh', token.get("refresh"))

        return response
