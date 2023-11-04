from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator, FileExtensionValidator
from shop.settings import MAX_IMAGE_UPLOAD_SIZE, MAX_IMAGE_UPLOAD_SIZE_VERBOSE, VALID_IMAGE_UPLOAD_EXTENSIONS
import re


class BaseFileExtensionValidator(FileExtensionValidator):
    """Базовый класс валидации расширения файла"""

    default_allowed_extensions = []

    def __init__(self, allowed_extensions=None, message=None, code=None):
        allowed_extensions = self.default_allowed_extensions
        message = f'Неверный формат файла. Разрешённые форматы: {", ".join(self.default_allowed_extensions)}'
        self.allowed_extensions_regex = self.get_allowed_extensions_regex()
        super().__init__(allowed_extensions, message, code)

    def get_allowed_extensions_regex(self) -> str:
        """Получение регулярки для валидации на стороне клиента"""

        return re.compile(f'(.|/)({"|".join(self.default_allowed_extensions)})$').pattern


class ImageFileExtensionValidator(BaseFileExtensionValidator):
    """Класс валидации расширения загружаемых файлов изображений"""

    default_allowed_extensions = VALID_IMAGE_UPLOAD_EXTENSIONS


class BaseMaxSizeValidator(MaxValueValidator):
    """Базовый класс валидации размера файлов"""

    max_value_size = MAX_IMAGE_UPLOAD_SIZE

    def __init__(self, limit_value=None, message=None):
        limit_value = self.max_value_size
        message = f'Размер файла не должен превышать {MAX_IMAGE_UPLOAD_SIZE_VERBOSE}.'
        super().__init__(limit_value, message)

    def compare(self, a, b):
        if a.size:
            return super().compare(a.size, b)


class FileMaxSizeValidator(BaseMaxSizeValidator):
    """Класс валидации размера загружаемых файлов"""

    max_value_size = MAX_IMAGE_UPLOAD_SIZE


class PasswordValidator(object):
    """Проверка пароля на соответствие требованиям"""

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


regex_name_pattern = re.compile(r'^[A-Za-zА-Яа-яёЁ -]{1,51}$', re.U)

name_validator = RegexValidator(
    regex_name_pattern,
    message='Для ввода доступны только латинские символы, кириллица, пробел, дефис.',
)

phone_validator = RegexValidator(
    regex=r'^(\+7)(\d{10})$',
    message='Укажите корректный номер в формате +7XXXXXXXXXX',
)
