from typing import Callable

from django.http import request, HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from common.repositories.base import BaseCRUDRepository


class BaseResponseAPIViewMixin:
    request: request.HttpRequest
    kwargs: request.QueryDict

    _response_class: Callable = Response


class ModelAPIViewMixin(BaseResponseAPIViewMixin):
    serializer_class: ModelSerializer
    _repository: BaseCRUDRepository

    def get_200_response(self, data: dict = None) -> Response:
        return self._response_class(
            data=data,
            status=status.HTTP_200_OK
        )

    def get_queryset(self, *args, **kwargs) -> None:
        pass


class POSTAPIViewMixin(BaseResponseAPIViewMixin):
    def get_request_data(self) -> dict:
        return self.request.POST


class ApiViewMixin:
    _response_class: Response = Response

    def get_200_response(self, data: dict):
        return self._response_class(
            data=data,
            status=status.HTTP_200_OK
        )


class DetailedApiViewMixin(ApiViewMixin):
    pk_url_kwarg: str

    def get_requested_pk(self) -> int:
        return self.kwargs.get(self.pk_url_kwarg)


class CreateAPIViewMixin(ModelAPIViewMixin, POSTAPIViewMixin):
    request: request.HttpRequest

    def get_201_response(self, data: dict = None):
        return self._response_class(
            data=data,
            status=status.HTTP_201_CREATED
        )


class RedirectViewMixin(ModelAPIViewMixin, POSTAPIViewMixin):
    request: request.HttpRequest

    @staticmethod
    def get_303_response(url: str) -> HttpResponseRedirect:
        return HttpResponseRedirect(
            redirect_to=url,
            status=status.HTTP_303_SEE_OTHER
        )
