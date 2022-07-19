from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .forms import VehicleForm, DriverForm,NewTownForm , CustomerRelationForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from .models import Town

from .models import Vehicle, Driver,CustomerRelation

from users.forms import User

# Create your views here.


UserManager = get_user_model()


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


class DriverListView(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = Driver
    context_object_name = 'drivers'
    template_name = 'driver_list.html'


class CreateDriverView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL
    template_name = 'driver.html'
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy('driver_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Driver'
        return context

    @atomic
    def form_valid(self, form):
        driver = form.save(commit=False)
        user = User()
        user.is_driver = True
        user.email = driver.email
        user.save()
        driver.users = user
        driver.save()
        return super().form_valid(form)


class UpdateDriverView(LoginRequiredMixin, UpdateView):
    login_url = settings.LOGIN_URL
    template_name = 'driver.html'
    success_url = reverse_lazy('driver_list')
    form_class = DriverForm
    model = Driver

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f'Update driver {self.object.name}'
        return ctx


class DeleteDriverView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request, pk):
        driver = get_object_or_404(Driver, pk=pk)
        driver.delete()
        return redirect('driver_list')



@login_required(login_url=settings.LOGIN_URL)
def town_list(request):
    context = {}
    context['towns'] = Town.objects.all()
    return render(request, 'town-list.html', context)

@login_required(login_url=settings.LOGIN_URL)
def town(request):
    context = {}
    context['towns'] = Town.objects.all()

    if request.method == 'POST':
        form = NewTownForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('town-list')
        else:
            context['form'] = form
            return render(request, 'town.html', context)

    else:
        form = NewTownForm()

    context['form'] = form

    return render(request, 'town.html', context)

@login_required(login_url=settings.LOGIN_URL)
def town_delete(request, pk):
    town = get_object_or_404(Town, pk=pk)
    town.delete()
    return redirect('town-list')

@login_required(login_url=settings.LOGIN_URL)
def town_edit(request, pk):
    town = get_object_or_404(Town, pk=pk)
    context = {}
    context['town'] = town
    form = NewTownForm()
    if request.method == 'POST':
        form = NewTownForm(request.POST, instance=town)
        if form.is_valid():
            form.save()
            return redirect('town-list')
    else:
        context['form'] = form
        return render(request, 'town-edit.html', context)
    
    
    
    



def create_customer(request):
    if request.method == 'POST':
        form = CustomerRelationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:customers')
    else:
        form = CustomerRelationForm()
    context = {"form": form}
    return render(request, 'tally/users/create_customer.html', context)


def list_customers(request):
    customers = CustomerRelation.objects.all()

    # Pagination
    paginator = Paginator(customers, 20)
    page = request.GET.get('page')

    print('page: ', page)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    context = {"customers": customers}
    return render(request, 'tally/users/customers_list.html', context)


def update_customer(request, pk):
    customer = get_object_or_404(CustomerRelation, pk=pk)
    if request.method == 'POST':
        form = CustomerRelationForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('users:customers')
    else:
        form = CustomerRelationForm(instance=customer)
    context = {'form': form}
    return render(request, 'tally/users/create_customer.html', context)


def delete_customer(request, pk):
    customer = get_object_or_404(CustomerRelation, pk=pk)
    customer.delete()
    return redirect('users:customers')
