from typing import Any, Optional, TypedDict

from django.http import HttpRequest
from profiles import models

class CreateUserPayload(TypedDict):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str


def create_user_profile(form: CreateUserPayload) -> models.User:
    user = models.User.objects.create_user(**form)
    models.Profile(user=user).save()
    return user

def profile_from_request(request: HttpRequest) -> models.Profile:
    return request.user.profile #type: ignore