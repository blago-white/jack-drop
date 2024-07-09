from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from schedule.repositories.schedule import ScheduleRepository


class AddItemToScheduleApiView(CreateAPIView):
    repository = ScheduleRepository()
    serializer_class = repository.default_serializer_class
    response_class = Response

    def create(self, request, *args, **kwargs):
        return self.get_response(data=self.repository.add(
            request_data=request.data
        ))

    def get_response(self, data: dict = None):
        return self.response_class(
            data=data,
            status=201
        )
