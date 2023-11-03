from django.contrib.auth.views import LoginView
from django.db.transaction import atomic
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django.contrib import messages
from django.conf import settings as django_settings
from accounts.forms import SignupForm, UserAuthenticationForm
from shop import settings


class SignupView(FormView):
    """Регистрация"""

    template_name = 'auth/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy(settings.SIGNUP_DONE_URL)

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

def verify(request, code):
    activated, message = settings.UserModel.verify_by_code(code)
    messages.add_message(request, (messages.constants.ERROR, messages.constants.SUCCESS)[activated], message)
    return redirect(django_settings.LOGIN_URL)


class UserLoginView(LoginView):
    """Аутентификация"""
    template_name = 'auth/login.html'
    form_class = UserAuthenticationForm
    # success_url = reverse_lazy(#)
    redirect_authenticated_user = True
