from .models import *
from django.forms import ModelForm

class CuentaForm(ModelForm):
    class Meta:
        model=Catalogocuenta
        fields=['numero','nombre']
class LibrodiarioForm(ModelForm):
    class Meta:
        model=Librodiario
        fields=['numero','fecha','numero_cuenta','debe','haber']
class LibromayorForm(ModelForm):
    class Meta:
        model=Libromayor
        fields=['numero_cuenta','fecha_inicio','fecha_fin','saldo_deudor','saldo_acreedor','saldo_final']