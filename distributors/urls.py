from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),

    path('vehicles/create', views.create_vehicle, name='vehicle'),
    path('vehicles/', views.vehicle_list, name='vehicle-list'),
    path('vehicles/<int:pk>', views.update_vehicle, name='vehicle-detail'),
    path('vehicles/delete/<int:pk>', views.delete_vehicle, name='vehicle-delete'),
    path('drivers/create', views.CreateDriverView.as_view(), name='driver'),
    path('drivers/', views.DriverListView.as_view(), name='driver_list'),
    path('drivers/<int:pk>', views.UpdateDriverView.as_view(), name='driver-detail'),
    path('drivers/delete/<int:pk>',
         views.DeleteDriverView.as_view(), name='driver-delete'),
    path('town/list/', views.town_list, name='town-list'),
    path('town/edit/<int:pk>', views.town_edit, name='town-edit'),
    path('town/create/', views.town, name='town'),
    path('town/delete/<int:pk>', views.town_delete, name='town-delete'),
    path('customers/', views.list_customers, name='customers'),
    path('customers/create', views.create_customer, name='customer-create'),
    path('customers/<int:pk>', views.update_customer, name='customer-update'),
    path('customers/delete/<int:pk>',
         views.delete_customer, name='customer-delete'),
    path('routes/create', views.route, name='route'),
    path('routes/', views.route_list, name='route_list'),
    path('routes/<int:pk>', views.route_delete, name='route_delete'),
    path('routes/delete/<int:pk>', views.update_route, name='route-detail'),


    path('valuers/', views.list_valuers, name='valuers'),
    path('valuers/create', views.create_valuer, name='valuer-create'),
    path('valuers/<int:pk>', views.update_valuer, name='valuer-update'),
    path('valuers/delete/<int:pk>', views.delete_valuer, name='valuer-delete'),
    
    















]
