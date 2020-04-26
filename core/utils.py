from typing import Union

from django.http import QueryDict


def format_form(POST: Union[QueryDict, dict], *args: str) -> dict:
    items = [item for item in args]
    items.extend(['csrfmiddlewaretoken'])
    return {key: value for key, value in POST.items() if key not in items}
