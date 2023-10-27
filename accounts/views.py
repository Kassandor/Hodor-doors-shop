from django.db.transaction import atomic
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from shop import settings


def index(request):
    return render(request, "base.html")


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
