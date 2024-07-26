from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from message.repositories.users import UsersApiRepository
from message.serializers import MessageSerializer
from message.mixins import MessagesApiViewMixin
from message.repositories.messages import MessagesRepository


class ChatMessagesListApiView(MessagesApiViewMixin, ListAPIView):
    repository = MessagesRepository()
    users_repository = UsersApiRepository()

    throttle_scope = "retrieve"
    throttle_classes = [ScopedRateThrottle]

    def list(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        return Response(
            data=self.repository.get_all(
                user_id=user_data.get("id"),
                username=user_data.get("username")
            )
        )


class ChatMessagesCreateApiView(MessagesApiViewMixin, CreateAPIView):
    repository = MessagesRepository()
    users_repository = UsersApiRepository()
    serializer_class = repository.default_serializer_class

    throttle_scope = "send"
    throttle_classes = [ScopedRateThrottle]

    def create(self, request, *args, **kwargs):
        user_data = self.users_repository.get(user_request=request)

        return Response(
            data=self.repository.add(
                user_id=user_data.get("id"),
                username=user_data.get("username"),
                text=request.data.get("text")
            ),
            status=201
        )
