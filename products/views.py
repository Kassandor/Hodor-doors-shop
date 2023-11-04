from django.views.generic import DetailView, ListView


class ProductDetail(DetailView):
    template_name = 'products/detail.html'


class ProductList(ListView):
    template_name = 'products/list.html'
