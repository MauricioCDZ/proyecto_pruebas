"""
    Se configuran las rutas de la aplicación web.
    Se asocian con las funciones en el archivo views.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name='login-signIn'),
    path('postSign/', views.postSign, name='login-welcome')
]