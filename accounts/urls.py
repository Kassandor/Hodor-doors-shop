from django.urls import path, re_path
from accounts.views import ProfileView, SignupView, signup_done, Verification, UserLoginView, UserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/done/', signup_done, name='signup-done'),
    re_path(
        r"^signup/verification/(?P<code>[a-zA-Z0-9_-]+)/$",
        Verification.as_view(),
        name="verify",
    ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
