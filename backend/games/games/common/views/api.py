from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView

from ..mixins.api.create import CreateApiViewMixin
from ..mixins.api.detail import DetailedApiViewMixin
from ..repositories import BaseRepository


class DefaultApiView(APIView):
    repository: BaseRepository


class DefaultRetrieveApiView(DetailedApiViewMixin,
                             DefaultApiView,
                             RetrieveAPIView):
    pass


class DefaultRetrieveCreateApiView(CreateApiViewMixin,
                                   DetailedApiViewMixin,
                                   DefaultApiView,
                                   RetrieveAPIView):
    pass


class DefaultCreateApiView(CreateApiViewMixin,
                           DefaultApiView,
                           CreateAPIView):
    pass
