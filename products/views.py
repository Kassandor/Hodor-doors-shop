from django.views.generic import DetailView, ListView

from cart.forms import CartAddProductForm
from products.models import Product


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'cart_product_form': CartAddProductForm(),
            }
        )
        return context


class ProductList(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'cart_product_form': CartAddProductForm(),
            }
        )
        return context
