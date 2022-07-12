from django.urls import path


from . import views
from .auth import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)
from . import auth

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


urlpatterns = [

    path("dashboard/", views.dashboard, name="dashboard"),




    path("login", LoginView.as_view(template_name='auth/login.html'), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    # path("login_success", LoginSuccess.as_view(), name="login_success_employee"),

    # path("logout", Logout.as_view(), name="logout_company"),
    path("password_reset", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "reset-password-sent/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password-complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # !


    path(
        'Password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='auth/password_change_form.html',
            success_url=reverse_lazy('password_change_done')
        ),
        name='password_change'
    ),


    path("password_change_done/", auth.change_done, name="password_change_done"),



]
