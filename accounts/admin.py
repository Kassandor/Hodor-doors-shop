from django.contrib import admin
from accounts.models import User, UserRole


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка: Пользователь"""

    pass


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    Админка: Роль пользователя
    """

    pass
