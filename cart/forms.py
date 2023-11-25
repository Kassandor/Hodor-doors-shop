from django.forms import Form, TypedChoiceField, BooleanField, HiddenInput


def get_product_quantity_choices(min=1, max=20):
    return [(i, str(i)) for i in range(min, max + 1)]


class CartAddProductForm(Form):
    quantity = TypedChoiceField(label='Количество', choices=get_product_quantity_choices(), coerce=int)
    update = BooleanField(required=False, initial=False, widget=HiddenInput)
