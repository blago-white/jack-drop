from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView

from common.mixins import BaseRetrieveApiViewMixin
from common.repositories import BaseRepository


class DefaultApiView(APIView):
    repository: BaseRepository


class DefaultRetrieveApiView(BaseRetrieveApiViewMixin,
                             RetrieveAPIView,
                             DefaultApiView):
    pass
