from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VehiculoForm


@login_required
def dashboard(request):
    return render(request,'dashboard.html')


@login_required
def registrar_vehiculo(request):

    if request.method == 'POST':
        form = VehiculoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = VehiculoForm()

    return render(request,'registrar.html',{'form':form})


@login_required
def vehiculos(request):
    return render(request,'vehiculos.html')


@login_required
def historial(request):
    return render(request,'historial.html')


@login_required
def reportes(request):
    return render(request,'reportes.html')


@login_required
def configuracion(request):
    return render(request,'configuracion.html')


@login_required
def modulo7(request):
    return render(request,'modulo7.html')


@login_required
def modulo8(request):
    return render(request,'modulo8.html')


@login_required
def modulo9(request):
    return render(request,'modulo9.html')


@login_required
def modulo10(request):
    return render(request,'modulo10.html')