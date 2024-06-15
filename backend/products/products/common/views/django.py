from django.views.generic import ListView
from ..services.base import BaseReadOnlyService


class BaseListView(ListView):
    _service: BaseReadOnlyService

    def get_queryset(self):
        print(self._service.get_all())
        return self._service.get_all()
