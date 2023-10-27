import re
from django.forms import PasswordInput, RegexField
from shop import settings


password_re = re.compile(settings.PASSWORD_RE_PATTERN, re.I)
error_msg = settings.PASSWORD_ERROR_MSG

class PasswordField(RegexField):
    widget = PasswordInput

    def __init__(self, regex=password_re, max_length=40, min_length=6, error_messages=error_msg, *args, **kwargs):
        super(PasswordField, self).__init__(
            regex=regex, max_length=max_length, min_length=min_length, error_messages=error_messages, *args, **kwargs
        )
