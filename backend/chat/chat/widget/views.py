from rest_framework.generics import ListAPIView
from django.views.generic import TemplateView

from message.services.messages import MessagesService, BaseMessagesService
from message.serializers import MessageSerializer

from .mixins import MessagesApiViewMixin


class ChatMessagesApiView(MessagesApiViewMixin, ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return self._service.get_all()


class ChatView(TemplateView):
    template_name = "chat.html"
