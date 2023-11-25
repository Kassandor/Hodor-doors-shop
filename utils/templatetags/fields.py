from django import template
from django.forms import BoundField

from utils.utils import get_logger

register = template.Library()


@register.inclusion_tag(filename='fields/field.html')
def field_group(bound_field: BoundField, label: str = None, required: bool = None, **kwargs):
    """
    Группа для поля ввода. Содержит поле и лейбл
    """
    if bound_field:
        label = label if label is not None else bound_field.label
        required = required if required is not None else bound_field.field.required

        field_type = type(bound_field.field.widget).__name__

        result = dict(field=bound_field, label=label, required=required, field_type=field_type)
        result.update(kwargs)
        return result
    else:
        get_logger(__name__).error(f'label="{label}" bound_field="{bound_field}"')


@register.inclusion_tag(filename='fields/_form_field.html')
def field(bound_field: BoundField, **kwargs):
    """
    Обёртка над инклудом поля ввода
    """
    result = dict(
        field=bound_field,
    )
    result.update(kwargs)
    return result