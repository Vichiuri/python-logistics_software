from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect, render


def dashboard(request):
    return render(request, "dashboard.html")
