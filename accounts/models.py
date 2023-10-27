from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from accounts.managers import UserManager
from utils.validators import name_validator, phone_validator
from accounts.mixins import UserRegistrationMixin
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

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user}'


class User(AbstractBaseUser, UserRegistrationMixin, PermissionsMixin):
    """Пользователь"""

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
    basket = models.OneToOneField(Basket, on_delete=models.PROTECT, related_name='user', null=True)
    is_staff = models.BooleanField("Администратор", default=False)
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=False,
        help_text='Активен ли пользователь (пройдена ли активация через email)',
    )
    date_joined = models.DateTimeField("Когда присоединился", default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'({self.email}), {self.first_name}'

    def get_username(self):
        return self.EMAIL_FIELD

    def save(self, *args, **kwargs):
        if not self.pk:
            # Создаём новую корзину
            new_basket = Basket.objects.create()
            self.basket = new_basket
        super(User, self).save(*args, **kwargs)
