from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from shop.settings import SUPPORT_EMAIL
from accounts.models import User


class SignupForm(forms.ModelForm):
    """Форма: Регистрация пользователя"""

    error_messages = {
        'password_mismatch': 'Пароли не совпадают. Повторите попытку.',
        'email_exists': 'Указанный email уже зарегистрирован',
    }

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-lg'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control form-control-lg'}),
        strip=False,
        help_text='Введите пароль еще раз',
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
        )
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_exists'])
        return email

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get(User.USERNAME_FIELD)
        if username:
            username = username.lower()
        return username


class UserAuthenticationForm(AuthenticationForm):
    """Форма: Аутентификация пользователя"""

    error_messages = {
        'invalid_login': 'Неверный пароль',
        'inactive': f'Пользователю запрещен доступ в систему, обратитесь в техническую поддержку: ',
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        try:
            super().clean()
            if not self.errors:
                return self.cleaned_data
        except forms.ValidationError as e:
            # Если пользователя не существует
            if username:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    raise forms.ValidationError(
                        {'username': 'Пользователь с таким логином не зарегистрирован'},
                        code=e.code,
                    )
                else:
                    if not user.is_active:
                        raise forms.ValidationError(
                            {'username': self.error_messages['inactive'] + SUPPORT_EMAIL},
                            code=e.code,
                        )
            # подменяем ошибки, чтобы они были привязаны к полю
            if e.code == 'invalid_login':
                raise forms.ValidationError(
                    {'password': self.error_messages['invalid_login']},
                    code=e.code,
                )
            else:
                raise e
