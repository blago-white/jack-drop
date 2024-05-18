from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from ..repositories import BaseRepository
from ..mixins.api.detail import DetailedApiViewMixin
from ..mixins.api.create import CreateApiViewMixin


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
