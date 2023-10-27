from django.contrib import admin
from django.urls import path, include
from shop.views import *


urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('admin/', admin.site.urls),
]
