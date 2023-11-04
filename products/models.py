from django.db import models


class Organization(models.Model):
    """Фирма"""

    name = models.CharField(verbose_name='Наименование', max_length=1000, unique=True)
    country = models.CharField(verbose_name='Страна', max_length=255)
    city = models.CharField(verbose_name='Город', max_length=255)

    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""

    name = models.CharField(verbose_name='Наименование', max_length=255, unique=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    organization = models.ForeignKey(
        Organization,
        verbose_name='Фирма',
        related_name='products',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
