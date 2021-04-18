from typing import TypeVar, Union

from django.http import QueryDict
from pydantic.main import BaseModel

T = TypeVar("T", bound=BaseModel)


def format_form(cls: type[T], form: QueryDict) -> T:
    return cls.parse_obj(form.dict())
