from django.views.generic import ListView

from ..services.base import BaseModelService


class BaseListView(ListView):
    _service: BaseModelService

    def get_queryset(self):
        print(self._service.get_all())
        return self._service.get_all()
