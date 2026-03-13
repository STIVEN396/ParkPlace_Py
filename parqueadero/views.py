from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from .models import Ingreso, Salida, Tarifa, Espacio
from django.db.models import Q


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
def salida(request):

    total = None
    placa = None
    tiempo = None

    if request.method == 'POST':

        placa = request.POST.get('placa')

        try:
            ingreso = Ingreso.objects.get(placa=placa)

            hora_salida = timezone.now()

            diferencia = hora_salida - ingreso.hora_ingreso
            segundos = diferencia.total_seconds()

            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)

            tiempo = f"{horas}h {minutos}m"

            tarifa = Tarifa.objects.get(
                tipo_vehiculo=ingreso.tipo_vehiculo
            )

            horas_decimal = segundos / 3600
            total = round(horas_decimal * float(tarifa.precio_hora), 2)

            Salida.objects.create(
                ingreso=ingreso,
                tiempo_total=horas_decimal,
                valor_pagado=total
            )

        except Ingreso.DoesNotExist:
            pass

    return render(request, 'salida.html', {
        'total': total,
        'placa': placa,
        'tiempo': tiempo
    })

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def vehiculos(request):
    return render(request, 'vehiculos.html')


@login_required
def historial(request):

    buscar = request.GET.get('buscar')

    ingresos = Ingreso.objects.all().order_by('-hora_ingreso')
    salidas = Salida.objects.all().order_by('-hora_salida')

    if buscar:
        ingresos = ingresos.filter(placa__icontains=buscar)
        salidas = salidas.filter(ingreso_placa_icontains=buscar)

    frecuentes = (
        Ingreso.objects
        .values('placa')
        .annotate(total=Count('placa'))
        .order_by('-total')[:5]
    )

    return render(request, 'historial.html', {
        'ingresos': ingresos,
        'salidas': salidas,
        'frecuentes': frecuentes,
        'buscar': buscar
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