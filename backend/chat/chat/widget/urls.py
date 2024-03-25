from django.urls import path
from .views import ChatMessagesApiView, ChatView


urlpatterns = [
    path("", ChatView.as_view(), name="chat"),
    path("api/v1/messages/",
         ChatMessagesApiView.as_view(),
         name="chat-messages")
]
