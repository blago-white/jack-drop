from django.conf import settings
from rest_framework.generics import RetrieveAPIView, CreateAPIView


class BaseGameProxyApiView(RetrieveAPIView):
    pass


class BaseGameProxyCreateApiView(CreateAPIView):
    pass
