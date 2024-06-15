from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView

from common.mixins import BaseRetrieveApiViewMixin, BaseDetailedCreateApiViewMixin
from common.repositories import BaseRepository


class DefaultApiView(APIView):
    repository: BaseRepository

    def get_queryset(self):
        return


class DefaultRetrieveApiView(BaseRetrieveApiViewMixin,
                             RetrieveAPIView,
                             DefaultApiView):
    pass


class DefaultCreateApiView(CreateAPIView,
                           DefaultApiView):
    pass


class DefaultUpdateApiView(BaseDetailedCreateApiViewMixin,
                           UpdateAPIView,
                           DefaultApiView):
    pass
