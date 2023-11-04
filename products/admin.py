from django.contrib import admin
from products.models import Product, Organization


@admin.register(Product)
class DoorAdmin(admin.ModelAdmin):
    """Админка: Дверь"""

    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Админка: Фирма"""

    pass
