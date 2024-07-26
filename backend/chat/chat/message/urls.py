from django.urls import path
from message.views import ChatMessagesListApiView, ChatMessagesCreateApiView


urlpatterns = [
    path("api/v1/messages/",
         ChatMessagesListApiView.as_view(),
         name="chat-messages-list"),
    path("api/v1/messages/create/",
         ChatMessagesCreateApiView.as_view(),
         name="chat-messages-create")
]
