from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ingreso


@login_required
def registrar_vehiculo(request):

    if request.method == 'POST':

        placa = request.POST.get('placa')
        tipo_vehiculo = request.POST.get('tipo_vehiculo')

        Ingreso.objects.create(
            placa=placa,
            tipo_vehiculo=tipo_vehiculo
        )

        return redirect('registrar')

    return render(request, 'registrar.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def vehiculos(request):
    return render(request, 'vehiculos.html')


from .models import Ingreso

@login_required
def historial(request):

    ingresos = Ingreso.objects.all().order_by('-hora_ingreso')

    return render(request, 'historial.html', {
        'ingresos': ingresos
    })

@login_required
def reportes(request):
    return render(request, 'reportes.html')


@login_required
def configuracion(request):
    return render(request, 'configuracion.html')


@login_required
def modulo7(request):
    return render(request, 'modulo7.html')


@login_required
def modulo8(request):
    return render(request, 'modulo8.html')


@login_required
def modulo9(request):
    return render(request, 'modulo9.html')


@login_required
def modulo10(request):
    return render(request, 'modulo10.html')