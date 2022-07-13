from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),

    path('vehicles/create', views.create_vehicle, name='vehicle'),
    path('vehicles/', views.vehicle_list, name='vehicle-list'),
    path('vehicles/<int:pk>', views.update_vehicle, name='vehicle-detail'),
    path('vehicles/delete/<int:pk>', views.delete_vehicle, name='vehicle-delete'),
]
