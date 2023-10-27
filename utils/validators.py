from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re


class PasswordValidator(object):
    """
    Проверка пароля на соответствие требованиям
    """

    min_length = 8
    code = 'password_not_secure'

    def validate(self, password: str, user=None):
        if user and user.is_superuser:
            self.min_length = 16
        # пароль длинный
        if len(password) < self.min_length:
            raise ValidationError(message=self.get_help_text(), code=self.code)

        # пароль содержит цифры
        if not any(char.isdigit() for char in password):
            raise ValidationError(message=self.get_help_text(), code=self.code)

        # пароль содержит прописные буквы
        if not any(char.isupper() for char in password):
            raise ValidationError(message=self.get_help_text(), code=self.code)

        # пароль содержит строчные буквы
        if not any(char.islower() for char in password):
            raise ValidationError(message=self.get_help_text(), code=self.code)

    def get_help_text(self):
        return f'Пароль должен содержать не менее {self.min_length} символов, строчные и прописные буквы и цифры.'


regex_name_pattern = re.compile(r"^[A-Za-zА-Яа-яёЁ -]{1,51}$", re.U)

name_validator = RegexValidator(
    regex_name_pattern,
    message="Для ввода доступны только латинские символы, кириллица, пробел, дефис.",
)

phone_validator = RegexValidator(
    regex=r"^(\+7)(\d{10})$",
    message="Укажите корректный номер в формате +7XXXXXXXXXX",
)
