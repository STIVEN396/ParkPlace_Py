from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from parqueadero.service.clienteServicio import ClienteServicio
from .models import Ingreso, Salida, Tarifa, Espacio, Usuario


@login_required
def registrar_vehiculo(request):

    if request.method == 'POST':

        placa = request.POST.get('placa')
        tipo_vehiculo = request.POST.get('tipo_vehiculo')

        # Verificar si el vehículo ya está dentro
        ingreso_abierto = Ingreso.objects.filter(
            placa=placa,
            salida__isnull=True
        ).first()

        if ingreso_abierto:
            messages.error(request, f"El vehículo {placa} ya está dentro del parqueadero")
            return redirect('registrar')

        Ingreso.objects.create(
            placa=placa,
            tipo_vehiculo=tipo_vehiculo,
            hora_ingreso=timezone.now()
        )

        messages.success(request, f"Vehículo {placa} registrado correctamente")
        return redirect('registrar')

    return render(request, 'gestion/registrar.html')


@login_required
def salida(request):

    total = None
    placa = None
    tiempo = None

    if request.method == 'POST':

        placa = request.POST.get('placa')

        # buscar ingreso que aún esté dentro
        ingreso = Ingreso.objects.filter(
            placa=placa,
            salida__isnull=True
        ).order_by('-hora_ingreso').first()

        # si no hay ingreso abierto
        if not ingreso:

            salida_registrada = Salida.objects.filter(
                ingreso__placa=placa
            ).order_by('-hora_salida').first()

            if salida_registrada:

                hora = salida_registrada.hora_salida.strftime("%H:%M")

                messages.error(
                    request,
                    f"El vehículo {placa} ya salió a las {hora}"
                )

            else:
                messages.error(
                    request,
                    "Ese vehículo no tiene registro de ingreso"
                )

            return redirect('salida')

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
            valor_pagado=total,
            hora_salida=hora_salida
        )

    return render(request, 'gestion/salida.html', {
        'total': total,
        'placa': placa,
        'tiempo': tiempo
    })


@login_required
def dashboard(request):
    return render(request, 'gestion/dashboard.html')


@login_required
def historial(request):
    cliente = ClienteServicio()
    datos = cliente.historial(request)

    return render(request, 'gestion/historial.html', datos)


@login_required
def reservas(request):
    return render(request, 'gestion/reservas.html')


@login_required
def gestion_espacios(request):
    return render(request, 'gestion/espacios.html')


@login_required
def tarifas(request):
    return render(request, 'gestion/tarifas.html')


@login_required
def usuarios(request):
    return render(request, 'gestion/usuarios.html')


@login_required
def reportes(request):
    return render(request, 'gestion/reportes.html')


@login_required
def configuracion(request):
    return render(request, 'gestion/configuracion.html')


def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            usuario = Usuario.objects.get(username=username)

            if check_password(password, usuario.password):

                request.session["usuario_id"] = usuario.id
                request.session["rol"] = usuario.rol

                return redirect("dashboard")

            else:
                messages.error(request, "Usuario o contraseña incorrectos")

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no existe")

    return render(request, "registration/login.html")
