from django.contrib.auth.views import LoginView, LogoutView
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, DetailView, RedirectView
from django.contrib import messages
from accounts.forms import SignupForm, UserAuthenticationForm
from shop.settings import (
    UserModel,
    SIGNUP_DONE_URL,
    LOGIN_URL,
)


class SignupView(FormView):
    """Регистрация"""

    template_name = 'auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy(SIGNUP_DONE_URL)

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.send_verification_mail()
        return super(SignupView, self).form_valid(form)


def signup_done(request):
    return render(request, 'auth/signup_done.html')


class Verification(RedirectView):
    """Верификация полученного кода"""

    permanent = False

    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")
        location = LOGIN_URL
        activated, message = UserModel.verify_by_code(code)
        messages.add_message(
            request,
            (messages.constants.ERROR, messages.constants.SUCCESS)[activated],
            message,
        )
        return redirect(location)


class UserLoginView(LoginView):
    """Аутентификация"""

    template_name = 'auth/login.html'
    form_class = UserAuthenticationForm
    # success_url = reverse_lazy(#)
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Выход из аккаунта"""

    template_name = 'auth/logout.html'


class ProfileView(DetailView):
    """Профиль пользователя"""

    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return UserModel.object.get(pk=self.request.user.id)
