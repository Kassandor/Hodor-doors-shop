from django import forms
from shop import settings
from utils.fields import PasswordField


class SignupForm(forms.ModelForm):
    error_messages = {'password_mismatch': 'Пароли не совпадают. Повторите попытку.'}

    password1 = PasswordField(label='Пароль')
    password2 = PasswordField(label='Введите пароль еще раз')

    class Meta:
        model = settings.UserModel
        fields = (settings.UserModel.USERNAME_FIELD,)

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
    username = self.cleaned_data.get(settings.UserModel.USERNAME_FIELD)
    if username:
        username = username.lower()
    return username


setattr(SignupForm, 'clean_%s' % settings.UserModel.USERNAME_FIELD, clean_username)
