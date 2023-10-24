from django.db import models


class Organization(models.Model):
    """Фирма"""

    name = models.CharField(
        verbose_name='Наименование', max_length=1000, unique=True
    )
    country = models.CharField(verbose_name='Страна', max_length=255)
    city = models.CharField(verbose_name='Город', max_length=255)


class Door(models.Model):
    """Дверь"""

    name = models.CharField(
        verbose_name='Наименование', max_length=255, unique=True
    )
    price = models.IntegerField(verbose_name='Цена')
    organization = models.ForeignKey(
        Organization,
        verbose_name='Фирма',
        related_name='doors',
        on_delete=models.CASCADE,
    )
