from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy

# Create your views here.


@login_required(login_url=settings.LOGIN_URL)
def project_index(request):

    return render(request, 'index.html')
