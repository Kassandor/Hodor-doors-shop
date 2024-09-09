from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from accounts.managers import UserManager
from utils.validators import name_validator, phone_validator
from accounts.mixins import UserRegistrationMixin
from products.models import Product


class UserRole(models.Model):
    """
    Роль пользователя
    """

    role = models.CharField(verbose_name='Роль', max_length=200, unique=True)

    def __str__(self):
        return self.role


class User(AbstractBaseUser, UserRegistrationMixin, PermissionsMixin):
    """
    Пользователь
    """

    role = models.ForeignKey(
        'accounts.UserRole', related_name='users', on_delete=models.SET_NULL, blank=True, null=True
    )
    first_name = models.CharField(verbose_name='Имя', max_length=255, validators=[name_validator])
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
        error_messages={'unique': 'Пользователь с таким адресом электронной ' 'почты уже зарегистрирован.'},
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=15,
        blank=True,
        null=True,
        help_text='Не обязательно',
        validators=[phone_validator],
    )
    is_staff = models.BooleanField("Администратор", default=False)
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=False,
        help_text='Активен ли пользователь (пройдена ли активация через email)',
    )
    date_joined = models.DateTimeField("Когда присоединился", default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def is_role(self, role):
        return self.role == role

    def is_trader(self):
        return self.is_role(UserRoleChoices.TRADER)

    def is_customer(self):
        return self.is_role(UserRoleChoices.CUSTOMER)

    def is_admin(self):
        return self.is_role(UserRoleChoices.ADMIN)

    def __str__(self):
        return f'({self.email}), {self.first_name}'

    def get_username(self):
        return self.EMAIL_FIELD
