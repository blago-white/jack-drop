from rest_framework.generics import ListAPIView, RetrieveAPIView

from ..mixins.api import ModelAPIViewMixin, DetailedApiViewMixin


class BaseListAPIView(ModelAPIViewMixin, ListAPIView):
    def list(self, request, *args, **kwargs):
        return self.get_200_response(data=self._repository.get_all())


class BaseRetreiveAPIView(DetailedApiViewMixin, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        object_pk = self.get_requested_pk()

        data = self._repository.get(pk=object_pk)

        return self.get_200_response(data=data)
