from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
class Catalogocuenta(models.Model):
    numero = models.CharField(max_length=2)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
class Librodiario(models.Model):
    numero=models.CharField(max_length=5)
    fecha = models.DateField()
    numero_cuenta = models.ForeignKey(Catalogocuenta, on_delete=models.CASCADE, null=False, blank=False)
    debe = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=12,validators=[MinValueValidator(Decimal('0.01'))])
    haber = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=12,validators=[MinValueValidator(Decimal('0.01'))])
    def __str__(self):
        return self.numero
class Libromayor(models.Model):
    numero_cuenta = models.ForeignKey(Catalogocuenta, on_delete=models.CASCADE, null=False, blank=False)
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    saldo_deudor = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=50,validators=[MinValueValidator(Decimal('0.00'))])
    saldo_acreedor = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=50,validators=[MinValueValidator(Decimal('0.00'))])
    saldo_final = models.DecimalField(blank=True,null=True,decimal_places=2,max_digits=50,validators=[MinValueValidator(Decimal('0.00'))])
    def __str__(self):
        return str(self.saldo_acreedor)
# Create your models here.
