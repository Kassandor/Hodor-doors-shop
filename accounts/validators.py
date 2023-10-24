from __future__ import unicode_literals
import re
from django.core.validators import RegexValidator


regex = re.compile(r"^[A-Za-zА-Яа-яёЁ -]{1,51}$", re.U)

name_validator = RegexValidator(
    regex,
    message="Для ввода доступны только латинские символы, кириллица, пробел, дефис.",
)

phone_validator = RegexValidator(
    regex=r"^(\+7)(\d{10})$",
    message="Укажите корректный номер в формате +7XXXXXXXXXX",
)
