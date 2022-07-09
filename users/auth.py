
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
     PasswordResetDoneView
from django.urls import reverse_lazy
from django.shortcuts import render
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
