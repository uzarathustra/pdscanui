"""pdscanui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from pdscanui import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('drive/', views.drive, name='drive'),
    path('drive/view_update_drive/', views.view_update_drive, name='view_update_drive'),
    path('drive/ajax/position/', views.updatePosition, name='update_Position'),
    path('transmitter_create/', views.transmitter_create, name='transmitter_create'),
    path('transmitter_list/', views.transmitter_list, name='transmitter_list'),
    path('transmitter_modify/<int:transmitter_pk>', views.transmitter_modify, name='transmitter_modify'),
    path('transmitter_modify/<int:transmitter_pk>/transmitter_delete', views.transmitter_delete, name='transmitter_delete'),
    path('transmitter_modify/<int:transmitter_pk>/transmitter_save', views.transmitter_save, name='transmitter_save'),
    path('receiver_create/', views.receiver_create, name='receiver_create'),
    path('receiver_list/', views.receiver_list, name='receiver_list'),
    path('receiver_modify/<int:receiver_pk>', views.receiver_modify, name='receiver_modify'),
    path('receiver_modify/<int:receiver_pk>/receiver_delete', views.receiver_delete, name='receiver_delete'),
    path('receiver_modify/<int:receiver_pk>/receiver_save', views.receiver_save, name='receiver_save'),
    path('measurement_create/', views.measurement_create, name='measurement_create'),
    path('measurement_list/', views.measurement_list, name='measurement_list'),
    path('measurement_modify/<int:measurement_pk>', views.measurement_modify, name='measurement_modify'),
    path('measurement_modify/<int:measurement_pk>/measurement_delete', views.measurement_delete, name='measurement_delete'),
    path('measurement_modify/<int:measurement_pk>/measurement_save', views.measurement_save, name='measurement_save'),
    path('measurement/', views.measurement, name='measurement'),
    path('results/', views.results, name='results'),
]
