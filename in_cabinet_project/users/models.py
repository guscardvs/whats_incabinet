from typing import Any, Optional, cast
from django.db import models, transaction
from django.contrib.auth import models as auth_md, get_user_model

from items.models import Item, UserItem
from users.dtos import RegisterDTO

# Create your models here.

_User = cast(type[auth_md.User], get_user_model())


class UserProxyManager(auth_md.UserManager):
    def create_user(
        self,
        username: str,
        email: Optional[str],
        password: Optional[str],
        **extra_fields: Any
    ) -> Optional["User"]:
        if self.filter(username=username).exists():
            return None
        else:
            return super().create_user(username, email, password, **extra_fields)


class User(_User):

    objects: "UserProxyManager[User]" = UserProxyManager()

    class Meta:
        proxy = True


class ProfileManager(models.Manager):
    def create(self, form: RegisterDTO) -> Optional["Profile"]:
        with transaction.atomic():
            user = User.objects.create_user(**form.dict())
            if not user:
                return None
            return super().create(user=user)


class Profile(models.Model):
    user: "models.OneToOneField[Profile, User]" = models.OneToOneField(
        to=User, on_delete=models.CASCADE
    )
    items = models.ManyToManyField(to=Item, related_name="profiles", through=UserItem)

    objects: ProfileManager = ProfileManager()