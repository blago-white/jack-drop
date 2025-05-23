"""
URL configuration for common project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import re_path, path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)

from accounts.api.private import TokenVerifyHeaderView

urlpatterns = [
    path(os.environ.get("ADMIN_PANEL_URL"), admin.site.urls),
    path('auth/', include("accounts.urls")),
    path('auth/discount/', include("promocodes.urls")),
    path('auth/referrals/', include("referrals.urls")),
    path('auth/balances/', include("balances.urls")),

    # path('auth/api/token/',
    #      TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    path('auth/api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/api/token/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),

    path('auth/api/token/_gateway_verify/',
         TokenVerifyHeaderView.as_view(),
         name='token_verify')
]

urlpatterns += [re_path(r'^i18n/', include('django.conf.urls.i18n'))]
