from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetDoneView
from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache


@sensitive_post_parameters()
@csrf_protect
@never_cache
def adminlogin(request):
    if request.method == "POST":

        print("Post")
        print(request.POST)
        user = authenticate(email=request.POST['email'],
                            password=request.POST['password'])

        if user is not None:
            print(user)
            login(request, user)
            messages.success(
                request, f"Login Successful, welcome {user.email}")
            return redirect(settings.LOGIN_REDIRECT_URL)

        else:
            return redirect(settings.LOGIN_URL)

    return render(request, 'login.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'auth/password_reset_form.html'

    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'


def change_done(request):
    return render(request, 'auth/password_change_done.html')
