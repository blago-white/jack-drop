from django.urls import path

from .api.endpoints import UserDiscountView

urlpatterns = [
    path("api/v1/p/get_user_discount/<int:user_id>/", UserDiscountView.as_view())
]
