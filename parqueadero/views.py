from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Espacio, Ingreso
from parqueadero.service.clienteServicio import ClienteServicio
from .models import Ingreso, Salida, Tarifa, Espacio, Usuario
import json
from .models import Reserva
from datetime import date

@login_required
def registrar_vehiculo(request):
    if request.method == 'POST':
        placa = request.POST.get('placa').strip().upper()
        tipo_vehiculo = request.POST.get('tipo_vehiculo')
        hoy = timezone.localdate()

        #Verificar si ya está dentro
        if Ingreso.objects.filter(placa=placa, salida__isnull=True).exists():
            messages.error(request, f"El vehículo {placa} ya está dentro")
            return redirect('registrar')

        #¿El que entra tiene reserva?
        from .models import Reserva
        reserva_activa = Reserva.objects.filter(
            placa__iexact=placa, 
            fecha=hoy, 
            estado='activa'
        ).first()

        espacios_libres = Espacio.objects.filter(
            tipo_vehiculo__iexact=tipo_vehiculo,
            estado='disponible'
        ).order_by('numero')

        if reserva_activa:
            espacio_disponible = espacios_libres.first()
        else:
            num_reservas = Reserva.objects.filter(fecha=hoy, estado='activa').count()
            #Intentamos tomar el espacio que sigue después de los reservados
            try:
                espacio_disponible = espacios_libres[num_reservas]
            except IndexError:
                #saltarse las reservas
                espacio_disponible = None

        if espacio_disponible:
            ingreso = Ingreso.objects.create(
                placa=placa,
                tipo_vehiculo=tipo_vehiculo,
                espacio=espacio_disponible
            )
            espacio_disponible.estado = 'ocupado'
            espacio_disponible.save()

            if reserva_activa:
                reserva_activa.estado = 'completada'
                reserva_activa.save()
                messages.success(request, f"Ingreso con reserva en espacio #{espacio_disponible.numero}")
            else:
                messages.success(request, f"Ingreso manual en espacio #{espacio_disponible.numero}")
        else:
            messages.error(request, "No hay espacios disponibles (están todos ocupados o reservados)")

        return redirect('registrar')

    return render(request, 'gestion/registrar.html')

@login_required
def salida(request):

    total = None
    placa = None
    tiempo = None

    if request.method == 'POST':
        placa = request.POST.get('placa')

        #Buscar ingreso que aún esté dentro
        ingreso = Ingreso.objects.filter(
            placa=placa,
            salida__isnull=True
        ).order_by('-hora_ingreso').first()

        if not ingreso:
            salida_registrada = Salida.objects.filter(
                ingreso__placa=placa
            ).order_by('-hora_salida').first()

            if salida_registrada:
                hora = salida_registrada.hora_salida.strftime("%H:%M")
                messages.error(request, f"El vehículo {placa} ya salió a las {hora}")
            else:
                messages.error(request, "Ese vehículo no tiene registro de ingreso")
            return redirect('salida')

        hora_salida = timezone.now()
        diferencia = hora_salida - ingreso.hora_ingreso
        segundos = diferencia.total_seconds()

        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        tiempo = f"{horas}h {minutos}m"

        tarifa = Tarifa.objects.get(tipo_vehiculo=ingreso.tipo_vehiculo)
        horas_decimal = segundos / 3600
        total = round(horas_decimal * float(tarifa.precio_hora), 2)

        #Registrar salida
        Salida.objects.create(
            ingreso=ingreso,
            tiempo_total=horas_decimal,
            valor_pagado=total,
            hora_salida=hora_salida
        )

        #Liberar espacio
        if ingreso.espacio:
            ingreso.espacio.estado = 'disponible'
            ingreso.espacio.save()

        messages.success(request, f"Vehículo {placa} salió correctamente. Total a pagar: ${total}")

    return render(request, 'gestion/salida.html', {
        'total': total,
        'placa': placa,
        'tiempo': tiempo
    })


@login_required
def dashboard(request):
    hoy = timezone.localdate()
    reservas_web_hoy = Reserva.objects.filter(fecha=hoy, estado='activa').count()
    total_espacios = Espacio.objects.count()
    ocupados = Espacio.objects.filter(estado='ocupado').count()
    disponibles_reales = total_espacios - ocupados - reservas_web_hoy
    disponibles = max(0, disponibles_reales)
    ingresos_hoy = Ingreso.objects.filter(hora_ingreso__date=hoy).count()
    ingresos = Ingreso.objects.filter(hora_ingreso__date=hoy)
    tipos_vehiculo_labels = list(set(ing.tipo_vehiculo for ing in ingresos))
    tipos_vehiculo_data = [sum(1 for ing in ingresos if ing.tipo_vehiculo == t) for t in tipos_vehiculo_labels]
    historial = Ingreso.objects.order_by('-hora_ingreso')[:10]

    for ingreso in historial:
        salida_qs = ingreso.salida_set.all()
        ingreso.hora_salida = salida_qs.last().hora_salida if salida_qs.exists() else None

    context = {
        'total_espacios': total_espacios,
        'ocupados': ocupados,
        'disponibles': disponibles,
        'reservados': reservas_web_hoy,
        'ingresos_hoy': ingresos_hoy,
        'tipos_vehiculo_labels': json.dumps(tipos_vehiculo_labels),
        'tipos_vehiculo_data': json.dumps(tipos_vehiculo_data),
        'historial': historial
    }

    return render(request, 'gestion/dashboard.html', context)


@login_required
def historial(request):
    cliente = ClienteServicio()
    datos = cliente.historial(request)

    return render(request, 'gestion/historial.html', datos)


@login_required

def reservas(request):
     return render(request, 'gestion/reservas.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Espacio

@login_required
def gestion_espacios(request):
    espacios = Espacio.objects.all().order_by('numero')
    hoy = timezone.localdate()
    
    #Traemos las reservas activas ordenadas por la hora en que se hicieron
    reservas_hoy = list(Reserva.objects.filter(fecha=hoy, estado='activa').order_by('id'))
    cantidad_reservas = len(reservas_hoy)
    
    idx_reserva = 0
    
    for espacio in espacios:
        if espacio.estado == 'ocupado':
            espacio.estado_visual = 'ocupado'
        elif idx_reserva < cantidad_reservas:
            #Si el espacio está disponible, le asignamos la reserva de forma fija
            espacio.estado_visual = 'reservado'
            espacio.placa_reserva = reservas_hoy[idx_reserva].placa
            idx_reserva += 1
        else:
            espacio.estado_visual = 'disponible'

    return render(request, 'gestion/espacios.html', {'espacios': espacios})


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

def crear_reserva(request):
    if request.method == 'POST':
        Reserva.objects.create(
            nombre=request.POST.get('nombre'),
            cedula=request.POST.get('cedula'),
            placa=request.POST.get('placa'),
            tipo_vehiculo=request.POST.get('tipo_vehiculo'),
            fecha=request.POST.get('fecha'),
            hora=request.POST.get('hora'),
        )

        messages.success(request, '¡Su reserva quedó registrada con éxito!')
        return redirect('crear_reserva') 
        
    return render(request, 'Reservaweb/crear_reserva.html')

def lista_reservas(request):
    #Traemos las reservas, las más nuevas primero
    reservas = Reserva.objects.all().order_by('-fecha', '-hora')
    
    return render(request, 'gestion/reservas.html', {'reservas': reservas})

def cancelar_reserva(request, reserva_id):
    try:
        reserva = Reserva.objects.get(id=reserva_id)
        reserva.estado = 'cancelada'
        reserva.save()
        messages.success(request, f"La reserva de {reserva.nombre} ha sido cancelada.")
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva no existe.")
        
    return redirect('ver_reservas')