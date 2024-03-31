from django.views.generic import ListView
from ..services.base import AbstractReadOnlyService


class BaseListView(ListView):
    _service: AbstractReadOnlyService

    def get_queryset(self):
        print(self._service.get_all())
        return self._service.get_all()
