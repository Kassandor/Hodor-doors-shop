from django.contrib import admin
from accounts.models import User, Basket


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка: Пользователь"""

    pass


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """Админка: Корзина"""

    pass
