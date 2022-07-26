from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import shortuuid
import datetime
import json
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .forms import VehicleForm, DriverForm, NewTownForm, CustomerRelationForm, RouteForm, ValuerForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from .models import Town
from django.db.models import Q

from .models import Vehicle, Driver, CustomerRelation, Route, Valuer, Document, ConsignmentNote

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
            return redirect('customers')
    else:
        form = CustomerRelationForm()
    context = {"form": form}
    return render(request, 'create_customer.html', context)


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
    return render(request, 'customers_list.html', context)


def update_customer(request, pk):
    customer = get_object_or_404(CustomerRelation, pk=pk)
    if request.method == 'POST':
        form = CustomerRelationForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CustomerRelationForm(instance=customer)
    context = {'form': form}
    return render(request, 'create_customer.html', context)


def delete_customer(request, pk):
    customer = get_object_or_404(CustomerRelation, pk=pk)
    customer.delete()
    return redirect('customers')


@login_required(login_url=settings.LOGIN_URL)
def route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm()

    return render(request, 'route.html', {'form': form})


@login_required(login_url=settings.LOGIN_URL)
def route_list(request):
    routes = Route.objects.all()
    return render(request, 'route_list.html', {'routes': routes})


@login_required(login_url=settings.LOGIN_URL)
def update_route(request, pk):

    route = get_object_or_404(Route, pk=pk)
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('route_list')
    else:
        form = RouteForm(instance=route)
    context = {'form': form}
    return render(request, 'route.html', context)


@login_required(login_url=settings.LOGIN_URL)
def route_delete(request, pk):
    route = get_object_or_404(Route, pk=pk)
    route.delete()
    return redirect('route_list')


def create_valuer(request):
    if request.method == 'POST':
        form = ValuerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('valuers')
    else:
        form = ValuerForm()
    context = {"form": form}
    return render(request, 'create_valuer.html', context)


def list_valuers(request):
    valuers = Valuer.objects.all()

    # Pagination
    paginator = Paginator(valuers, 20)
    page = request.GET.get('page')

    print('page: ', page)

    try:
        valuers = paginator.page(page)
    except PageNotAnInteger:
        valuers = paginator.page(1)
    except EmptyPage:
        valuers = paginator.page(paginator.num_pages)

    context = {"valuers": valuers}
    return render(request, 'valuers_list.html', context)


def update_valuer(request, pk):
    valuer = get_object_or_404(Valuer, pk=pk)
    if request.method == 'POST':
        form = ValuerForm(request.POST, instance=valuer)
        if form.is_valid():
            form.save()
            return redirect('valuers')
    else:
        form = ValuerForm(instance=valuer)
    context = {'form': form}
    return render(request, 'create_valuer.html', context)


def delete_valuer(request, pk):
    valuer = get_object_or_404(Valuer, pk=pk)
    valuer.delete()
    return redirect('valuers')


@login_required(login_url=settings.LOGIN_URL)
def note(request):
    context = {}

    reference_no = ConsignmentNote.objects.all().order_by('-id').first()

    if reference_no is not None:
        reference_no = shortuuid.ShortUUID().random(length=8)
        tracking_no = ConsignmentNote.objects.all().order_by('-id').first().tracking_no + 1
    else:
        tracking_no = 1
        reference_no = shortuuid.ShortUUID().random(length=8)

    context['reference_no'] = reference_no
    context['tracking_no'] = tracking_no

    if "action" in request.GET.keys():
        action = request.GET['action']
        if action == 'get_routes':
            q = request.GET['q']
            routes = Route.objects.filter(Q(route_name__icontains=q))

            if routes is None:
                return JsonResponse({
                    'routes': []
                }, safe=False)

            return JsonResponse({
                'routes': [{'text': route.route_name, 'id': route.id} for route in routes]
            }, safe=False)

    if "action" in request.GET.keys():
        action = request.GET['action']
        if action == 'get_towns':
            q = request.GET['q']
            towns = Town.objects.filter(Q(name__icontains=q))

            if towns is None:
                return JsonResponse({
                    'towns': []
                }, safe=False)

            return JsonResponse({
                'towns': [{'text': route.name, 'id': route.id} for route in towns]
            }, safe=False)

    if "action" in request.GET.keys():
        action = request.GET['action']
        if action == 'get_documents':
            documents = Document.objects.all()

            if documents is None:
                return JsonResponse({
                    'documents': []
                }, safe=False)

            return JsonResponse({
                'documents': [{'name': document.doc_name, 'id': document.id} for document in documents]
            }, safe=False)

    if "action" in request.GET.keys():
        action = request.GET['action']
        if action == 'get_customers':
            try:
                q = request.GET['q']
                sender_id = request.GET['sender_id']
            except KeyError:
                q = ''

            print('Sender id: ', sender_id)
            print('Sender id: ', type(sender_id))

            if sender_id == '1':
                # search for senders only
                customers = CustomerRelation.objects.filter(
                    Q(customer_name__icontains=q)
                )
            else:
                customers = CustomerRelation.objects.filter(
                    Q(customer_name__icontains=q), ~Q(id=sender_id)
                )

            if customers is None:
                return JsonResponse({
                    'customers': []
                }, safe=False)

            return JsonResponse({
                'customers': [{'text': customer.customer_name, 'id': customer.id} for customer in customers]
            }, safe=False)

    if "action" in request.GET.keys():
        action = request.GET['action']
        if action == 'get_valuers':
            q = request.GET['q']
            valuers = UserManager.objects.filter(
                Q(is_valuer=True) & Q(name__icontains=q))

            if valuers is None:
                return JsonResponse({
                    'valuers': []
                }, safe=False)

            return JsonResponse({
                'valuers': [{'text': valuer.name, 'id': valuer.id} for valuer in valuers]
            }, safe=False)

    if request.method == 'POST':
        # SAVE ROUTES
        if "action" in request.GET.keys():
            action = request.GET['action']
            if action == 'save_routes':
                # get data from form data
                route_name = request.POST['route_name']
                print(route_name)
                try:
                    route = Route.objects.create(
                        route_name=route_name,
                    )
                    route.save()
                    return JsonResponse({
                        'success': True,
                        'route': {'text': route.route_name, 'id': route.id}
                    }, safe=False)
                except KeyError:
                    return JsonResponse({
                        'success': False,
                        'route': {}
                    }, safe=False)

        if "action" in request.GET.keys():
            action = request.GET['action']
            if action == 'save_towns':
                # get data from form data
                town_name = request.POST['town_name']
                try:
                    town = Town.objects.create(
                        name=town_name,
                    )
                    town.save()
                    return JsonResponse({
                        'success': True,
                        'town': {'text': town.name, 'id': town.id}
                    }, safe=False)
                except KeyError:
                    return JsonResponse({
                        'success': False,
                        'town': {}
                    }, safe=False)

        if "action" in request.GET.keys():
            action = request.GET['action']
            if action == 'save_consignee':
                # get data from form data
                consignee_name = request.POST['consignee_name']
                consignee_address = request.POST['consignee_address']
                consignee_pin = request.POST['consignee_pin']
                consignee_account = request.POST['consignee_account']

                if consignee_address == '':
                    consignee_address = None

                if consignee_pin == '':
                    consignee_pin = None

                if consignee_account == '':
                    consignee_account = None

                try:
                    customer = CustomerRelation.objects.create(
                        customer_name=consignee_name,
                        customer_address=consignee_address,
                        Customer_pin=consignee_pin,
                        account=consignee_account,
                    )
                    customer.save()

                    return JsonResponse({
                        'success': True,
                        'consignee': {'text': customer.customer_name, 'id': customer.id}
                    }, safe=False)
                except KeyError:
                    return JsonResponse({
                        'success': False,
                        'consignee': {}
                    }, safe=False)

        if "action" in request.GET.keys():
            action = request.GET['action']
            if action == 'save_sender':
                # get data from form data
                consignee_name = request.POST['sender_name']
                consignee_address = request.POST['sender_address']
                consignee_pin = request.POST['sender_pin']
                consignee_account = request.POST['sender_account']

                if consignee_address == '':
                    consignee_address = None

                if consignee_pin == '':
                    consignee_pin = None

                if consignee_account == '':
                    consignee_account = None

                try:
                    customer = CustomerRelation.objects.create(
                        customer_name=consignee_name,
                        customer_address=consignee_address,
                        Customer_pin=consignee_pin,
                        account=consignee_account,
                    )
                    customer.save()

                    return JsonResponse({
                        'success': True,
                        'sender': {'text': customer.customer_name, 'id': customer.id}
                    }, safe=False)
                except KeyError:
                    return JsonResponse({
                        'success': False,
                        'sender': {}
                    }, safe=False)

        id_delivered = False
        if request.POST['id_delivered'] == 'true':
            id_delivered = True

        if request.POST['input'] == '0':

            customer_sender = CustomerRelation(
                customer_name=request.POST['sender_name'],
            )

            customer_sender.save()

            customer_consignee = CustomerRelation(
                customer_name=request.POST['sender_name'],
                created=True
            )

            customer_consignee.save()

            # route = Route(
            #     route_name=request.POST['route'],
            #     created=True
            # )

            route.save()

            town = Town(
                name=request.POST['town'],
                created=True
            )

            town.save()

            note = ConsignmentNote(
                tracking_no=request.POST['tracking_no'],
                sender_name=customer_sender,
                consignee=customer_consignee,
                description=request.POST['description'],
                quantity=request.POST['quantity'],
                per=request.POST['per'],
                town=town,
                amount=int(float(request.POST['exclusive'])),
                tax=int(float(request.POST['tax'])),
                inclusive=int(float(request.POST['inclusive'])),
                bundle=request.POST['bundle'],
                rate=request.POST['rate'],
                reference_no=request.POST['reference_no'],
                is_delivered=id_delivered,
                route=Route.objects.get(pk=request.POST['route']),
                date_created=datetime.datetime.now().date(),
                document=Document.objects.get(pk=request.POST['document']),
                valuer=UserManager.objects.get(pk=request.POST['valuer'])
            )
            note.save()

        else:
            note = ConsignmentNote(
                tracking_no=request.POST['tracking_no'],
                sender_name=CustomerRelation.objects.get(
                    id=request.POST['sender_name']),
                consignee=CustomerRelation.objects.get(
                    id=request.POST['consignee']),
                description=request.POST['description'],
                quantity=request.POST['quantity'],
                town=Town.objects.get(id=request.POST['town']),
                per=request.POST['per'],
                amount=int(float(request.POST['exclusive'])),
                tax=int(float(request.POST['tax'])),
                inclusive=int(float(request.POST['inclusive'])),
                bundle=request.POST['bundle'],
                rate=request.POST['rate'],
                reference_no=request.POST['reference_no'],
                is_delivered=id_delivered,
                date_created=datetime.datetime.now().date(),
                route=Route.objects.get(pk=request.POST['route']),
                document=Document.objects.get(pk=request.POST['document']),
                valuer=UserManager.objects.get(pk=request.POST['valuer'])
            )
            note.save()

        return JsonResponse(
            {
                'status': 'success',
                'id': note.id
            }
        )

    return render(request, 'note.html', context)
