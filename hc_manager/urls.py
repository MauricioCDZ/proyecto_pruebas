"""hc_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from django.urls import path, include

urlpatterns = [
    path('admin/', views.admin, name="app-admin"),
    path('adminHC/', views.adminHC, name='app-adminHC'),
    path('adminUser/', views.adminUser, name='app-adminUser'),
    path('adminCreate/', views.adminCreate, name='app-adminCreate'),
    path('adminEdit/<slug:cedula>/', views.adminEdit, name='app-adminEdit'),
    path('adminLog/<slug:cedula>/', views.adminLog, name='app-adminLog'),
    path('adminCita/<slug:cedula>/', views.adminCita, name='app-adminCita'),
    path('adminDelHC/<slug:cedula>/', views.adminDelHC, name='app-adminDelHC'),
    path('', include('login.urls'), name='app-home'),
    path('newHC/', views.newHC, name='app-newHC'),
    path('editHC/<slug:cedula>/', views.editHC, name='app-editHC'),
    path('logHC/<slug:cedula>/', views.logHC, name='app-logHC'),
    path('newCita/<slug:cedula>/', views.newCita, name='app-newCita'),
    path('help/', views.help, name='app-help')
]