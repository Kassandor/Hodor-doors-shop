from django.contrib import admin
from products.models import Door, Organization


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    """Админка: Дверь"""

    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Админка: Фирма"""

    pass
