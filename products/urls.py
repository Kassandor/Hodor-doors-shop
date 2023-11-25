from django.urls import path
from products.views import ProductList, ProductDetail

app_name = 'products'

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
]
