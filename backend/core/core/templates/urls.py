from django.urls import path

from .views import main_page_view, account_view


urlpatterns = [
    path("", main_page_view),
    path("account/", account_view, name="account")
]
