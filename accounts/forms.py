from django import forms
from django.contrib.auth import password_validation
from accounts.models import User


class SignupForm(forms.ModelForm):
    """Форма: Регистрация пользователя"""

    error_messages = {'password_mismatch': 'Пароли не совпадают. Повторите попытку.'}

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text='Enter the same password as before, for verification',
    )

    class Meta:
        model = User
        fields = (
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
            'phone',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data.get(User.USERNAME_FIELD)
        if username:
            username = username.lower()
        return username
