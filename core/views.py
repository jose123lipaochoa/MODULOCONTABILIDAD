from django.shortcuts import render, redirect
from .forms import *
from .models import *

def cuentas(request):
    cuentas= Catalogocuenta.objects.all()
    return render(request,'core/cuenta.html',{'cuentas':cuentas})

def librodiario(request):
    librodiarios=Librodiario.objects.all()
    return render(request,'core/librodiario.html',{'librodiarios':librodiarios})

def registrardiario(request):
    form = LibrodiarioForm()
    cuentas=Catalogocuenta.objects.all()
    if (request.method=='POST'):
        print('Printin POST:',request.POST)
        form=LibrodiarioForm(request.POST)
        if (form.is_valid()):
            form_data=form.cleaned_data
            if(form_data.get('debe') and form_data.get('haber') or Librodiario.objects.filter(numero=form_data.get('numero')).count()>0):
                return redirect('registrardiario')
            try:
                if(int(form_data.get('numero'))>0):
                    form.save()
                    return redirect('librodiario')
            except:
                return redirect('registrardiario')
    context={'form':form,'cuentas':cuentas}
    return render(request,'core/registrardiario.html',context)
def libromayor(request):
    form = LibromayorForm()
    cuentas=Catalogocuenta.objects.all()
    instance=''
    if (request.method == "POST"):
        print('Printin POST:',request.POST)
        form=LibromayorForm(request.POST)
        if(form.is_valid()):
            form_data=form.cleaned_data
            if(form_data.get('fecha_fin')>=form_data.get('fecha_inicio')):
                diarios=Librodiario.objects.filter(
                    fecha__gte=form_data.get('fecha_inicio'),
                    fecha__lte=form_data.get('fecha_fin'),
                    numero_cuenta=form_data.get('numero_cuenta')
                )
                if (diarios):
                    instance = Libromayor.objects.create(
                        numero_cuenta=form_data.get('numero_cuenta'),
                        fecha_fin=form_data.get('fecha_fin'),
                        fecha_inicio=form_data.get('fecha_inicio'),
                        saldo_acreedor=Decimal(0.00),
                        saldo_deudor=Decimal(0.00),
                        saldo_final=Decimal(0.00)
                    )
                    haber_total=Decimal(0.00)
                    debe_total=Decimal(0.00)
                    for diario in diarios:
                        if (diario.haber):
                            haber_total=haber_total+diario.haber
                        else:
                            debe_total=debe_total+diario.debe
                    if(haber_total>debe_total):
                        instance.saldo_acreedor= haber_total-debe_total
                        instance.saldo_final= haber_total-debe_total
                    if(haber_total<debe_total):
                        instance.saldo_acreedor= debe_total-haber_total
                        instance.saldo_final= debe_total-haber_total
                    if(haber_total==debe_total):
                        instance.saldo_final= debe_total-haber_total
                    form = LibrodiarioForm(request.POST, instance=instance)
                    print('Printin POST:', request.POST)
                    if (form.is_valid()):
                        form.save()
    context={'form':form, 'cuentas':cuentas, 'instance':instance}
    return render(request,'core/libromayor.html',context)

def eliminardiario(request,numero):
    libro=Librodiario.objects.get(numero=numero)
    if (request.method=="POST"):
        libro.delete()
        return redirect('librodiario')
    context={'item':libro}
    return render(request,'core/eliminardiario.html',context)

def editardiario(request,numero):
    cuentas=Catalogocuenta.objects.all()
    diario = Librodiario.objects.get(numero=numero)
    form = LibrodiarioForm(instance=diario)
    if (request.method == 'POST'):
        print('Printin POST:', request.POST)
        form = LibrodiarioForm(request.POST, instance=diario)
        if (form.is_valid()):
            form_data = form.cleaned_data
            if (form_data.get('debe') and form_data.get('haber') or Librodiario.objects.filter(
                    numero=form_data.get('numero')).count() > 0):
                return redirect(request.get_full_path())
            try:
                if (int(form_data.get('numero')) > 0 and numero==form_data.get('numero')):
                    form.save()
                    return redirect('librodiario')
                else:
                    if (int(form_data.get('numero')) > 0 and Librodiario.objects.filter(numero=form_data.get('numero')).count() == 0):
                        form.save()
                        return redirect('librodiario')
            except:
                return redirect(request.get_full_path())
    context = {'form': form,'cuentas':cuentas}
    return render(request, 'core/editardiario.html', context)



def periodo(request):
    return render(request,'core/periodo.html')

def registrarcuentas(request):
    form = CuentaForm()
    if (request.method=='POST'):
        print('Printin POST:',request.POST)
        form=CuentaForm(request.POST)
        if (form.is_valid()):
            form_data=form.cleaned_data
            try:
                int(form_data.get('nombre'))
            except:
                try:
                    if(int(form_data.get('numero')) > 0):
                        if (Catalogocuenta.objects.filter(numero=form_data.get('numero')).count() == 0):
                            form.save()
                            return redirect('/')
                except:
                    message="error"
    context={'form':form}
    return render(request,'core/registrarcuentas.html',context)

def editarcuentas(request,numero):
    cuenta=Catalogocuenta.objects.get(numero=numero)
    form= CuentaForm(instance=cuenta)
    if (request.method=='POST'):
        print('Printin POST:',request.POST)
        form=CuentaForm(request.POST,instance=cuenta)
        if (form.is_valid()):
            form_data=form.cleaned_data
            try:
                int(form_data.get('nombre'))
            except:
                try:
                    if (int(form_data.get('numero')) > 0 and numero==form_data.get('numero')):
                        form.save()
                        return redirect('/')
                    else:
                        if(int(form_data.get('numero')) > 0 and Catalogocuenta.objects.filter(numero=form_data.get('numero')).count()==0):
                            form.save()
                            return redirect('/')
                except:
                    message = "error"
    context = {'form': form}
    return render(request,'core/editarcuentas.html',context)

