from common.mixins import BaseModelApiViewMixin
from message.services.messages import MessagesService


class MessagesApiViewMixin(BaseModelApiViewMixin):
    _service = MessagesService()
