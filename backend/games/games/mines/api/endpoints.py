from common.views.api import DefaultCreateApiView

from mines.repositories.mines import MinesGameRepository


class MakeGameView(DefaultCreateApiView):
    repository = MinesGameRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.make(request_data=request.data)
        )
