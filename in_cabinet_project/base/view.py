from functools import partial, wraps
from typing import Callable, Generic, Optional, TypeVar, Union, get_type_hints, get_args
from django.http.response import HttpResponse
from django.views import View
from django.http import HttpRequest, request
from pydantic import ValidationError
from inspect import isfunction, signature
from django.shortcuts import redirect, render
from pydantic.main import BaseModel
from base.exception import ViewException
from dataclasses import dataclass
from base import utils
from enum import Enum

T = TypeVar("T", bound=BaseModel)


@dataclass
class RequestWrapper(Generic[T]):
    request: HttpRequest
    schema: type[T]

    def form(self) -> T:
        return utils.format_form(self.schema, self.request.POST)


class decoratedview:
    def __init__(
        self,
        *,
        template_name: Optional[str] = None,
        custom_response: bool = False,
    ) -> None:
        self.template_name = template_name
        self.custom_response = custom_response

    def __call__(self, func):
        return self._decorate(func)

    def _decorate(decorator, func: Callable[..., Union[dict, HttpResponse, str, None]]):
        @wraps(func)
        def inner(self: "PydanticView", request, *args, **kwargs):
            try:
                kwargs = decorator.parse_kwargs(request, func, kwargs)
                result = func(self, *args, **kwargs)
            except (ValidationError, ViewException) as err:
                result = self._error(request, err)
            return decorator.get_response(self, request, result)

        return inner

    @staticmethod
    def parse_kwargs(request: HttpRequest, func: Callable, kwargs: dict):
        hints = get_type_hints(func)
        if "wrapper" in hints:
            if result := get_args(hints["wrapper"]):
                (schema_t,) = result
                kwargs["wrapper"] = RequestWrapper(request, schema_t)
        if "request" in signature(func).parameters:
            kwargs["request"] = request
        return kwargs

    def get_response(
        self,
        py_view: "PydanticView",
        request: HttpRequest,
        result: Union[dict, HttpResponse, str, None],
    ):
        if (
            not isinstance(result, dict)
            and not isinstance(result, HttpResponse)
            and not isinstance(result, str)
            and result is not None
        ):
            raise NotImplementedError
        if self.custom_response:
            return result
        return self._guess_response(py_view, request, result)

    def _guess_response(
        self,
        py_view: "PydanticView",
        request: HttpRequest,
        result: Union[dict, HttpResponse, str, None],
    ):
        template_name = py_view.template_name
        if self.template_name is not None:
            template_name = self.template_name
        if isinstance(result, dict):
            return render(request, template_name, context=result)
        if isinstance(result, HttpResponse):
            return result
        if isinstance(result, str):
            return redirect(result)
        if result is None:
            return render(request, template_name)


class PydanticView(View):
    template_name: str

    @decoratedview()
    def error(
        self, request: HttpRequest, errors: list[Union[ValidationError, ViewException]]
    ):
        return

    def _error(self, request: HttpRequest, err: Union[ValidationError, ViewException]):
        if isinstance(err, ValidationError):
            return self.error(request, [item.exc for item in err.raw_errors])
        else:
            return self.error(request, [err])
