from django.http.request import HttpRequest

from common.views.api import DefaultCreateApiView

from mines.repositories.mines import MinesGameRepository


class MakeGameView(DefaultCreateApiView):
    repository = MinesGameRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        return self.get_201_response(
            data=self.repository.init(data=request.data)
        )


class NextStepMinesGameView(DefaultCreateApiView):
    repository = MinesGameRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request: HttpRequest, *args, **kwargs):
        try:
            data = self.repository.next(
                request_data=request.data
            )
        except Exception as e:
            raise e

            data = None

        return self.get_201_response(
            data=data
        )


class StopMinesGameView(DefaultCreateApiView):
    repository = MinesGameRepository()
    serializer_class = repository.default_serializer_class

    def create(self, request, *args, **kwargs):
        print("DELETE")
        try:
            return self.get_201_response(
                data=self.repository.stop(
                    user_id=self.request.data.get("user_id")
                )
            )
        except Exception as e:
            raise e
