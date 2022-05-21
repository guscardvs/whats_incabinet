from typing import Union

from django.http import QueryDict


def pop_csrf(POST: Union[QueryDict, dict], *args: str) -> dict:
    items = (*args, 'csrfmiddlewaretoken')
    return {key: value for key, value in POST.items() if key not in items}
