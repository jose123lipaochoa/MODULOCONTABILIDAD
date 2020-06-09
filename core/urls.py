from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', cuentas, name="cuenta"),
    path('registrarcuentas', registrarcuentas, name="registrarcuentas"),
    path('editarcuentas/<str:numero>', editarcuentas, name="editarcuentas"),
    path('editardiario/<str:numero>', editardiario, name="editardiario"),
    path('librodiario', librodiario, name="librodiario"),
    path('registrardiario', registrardiario, name="registrardiario"),
    path('eliminardiario/<str:numero>', eliminardiario, name="eliminardiario"),
    path('libromayor', libromayor, name="libromayor"),
]