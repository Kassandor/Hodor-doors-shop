from django.views.generic import DetailView, ListView

from products.models import Product


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'
    context_object_name = 'products'
