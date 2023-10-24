from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from accounts.validators import phone_validator, name_validator
from products.models import Door


class Basket(models.Model):
    """Корзина"""

    doors = models.ManyToManyField(
        Door,
        related_name='doors',
        related_query_name='door',
        blank=True,
        null=True,
    )


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователь"""

    first_name = models.CharField(
        verbose_name='Имя', max_length=255, validators=[name_validator]
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255,
        blank=True,
        null=True,
        validators=[name_validator],
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
        db_index=True,
        error_messages={
            'unique': 'Пользователь с таким адресом электронной '
            'почты уже зарегистрирован.'
        },
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=15,
        blank=True,
        null=True,
        help_text='Не обязательно',
        validators=[phone_validator],
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=False,
        help_text=(
            'Активен ли пользователь (пройдена ли активация через email)'
        ),
    )
    basket = models.OneToOneField(
        Basket, on_delete=models.SET_NULL, related_name='user'
    )
