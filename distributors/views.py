from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .forms import VehicleForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse


from .models import Vehicle

# Create your views here.


@login_required(login_url=settings.LOGIN_URL)
def project_index(request):

    return render(request, 'index.html')


@login_required(login_url=settings.LOGIN_URL)
def create_vehicle(request):

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("vehicle-list")
    else:
        form = VehicleForm()
    context = {'form': form}
    return render(request, 'vehicle.html', context)


@login_required(login_url=settings.LOGIN_URL)
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


@login_required(login_url=settings.LOGIN_URL)
def update_vehicle(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle-list')
    else:
        form = VehicleForm(instance=vehicle)
    context = {'form': form}
    return render(request, 'vehicle.html', context)


@login_required(login_url=settings.LOGIN_URL)
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('vehicle-list')
