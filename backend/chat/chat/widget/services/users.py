from abc import ABCMeta, abstractmethod

from django.http.request import HttpRequest


class BaseUserService(metaclass=ABCMeta):
    @abstractmethod
    def get_username(self, request: HttpRequest):
        # TODO: Integrate auth backends with users service
        return request.headers.get("Authorization")
