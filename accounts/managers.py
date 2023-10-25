from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from django.utils import timezone

class UserQueryset(models.QuerySet):
    """Кверисет: Пользователь"""

    def active(self):
        return self.filter(is_active=True)


class UserManager(DjangoUserManager):
    """Менеджер: Пользователь"""

    def get_queryset(self):
        return UserQueryset(model=self.model)

    def create_superuser(self, email, *args, **kwargs):
        return super(UserManager, self).create_superuser(email, email, *args, **kwargs)

    def _create_user(
        self,
        username,
        email,
        password,
        is_staff,
        is_superuser,
        basket=None,
        is_active=True,
        **extra_fields,
    ):
        # Создаём пользователя без username
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            basket=basket,
            is_active=is_active,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return super(UserManager, self).create_user(
            email, email, password, **extra_fields
        )
