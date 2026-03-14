from django.db import models
from django.utils import timezone


class Espacio(models.Model):
    numero = models.IntegerField()
    tipo_vehiculo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, default='disponible')

    def __str__(self):
        return f"Espacio {self.numero} ({self.estado})"


class Tarifa(models.Model):
    tipo_vehiculo = models.CharField(max_length=20)
    precio_hora = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        return f"{self.tipo_vehiculo} - {self.precio_hora}"


class Ingreso(models.Model):
    placa = models.CharField(max_length=10)
    tipo_vehiculo = models.CharField(max_length=20)
    espacio = models.ForeignKey(Espacio, on_delete=models.SET_NULL, null=True)
    hora_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.placa

    def asignar_espacio(self):
        # Busca un espacio disponible para el tipo de vehículo
        espacio_disponible = Espacio.objects.filter(
            tipo_vehiculo=self.tipo_vehiculo,
            estado='disponible'
        ).first()
        if espacio_disponible:
            self.espacio = espacio_disponible
            espacio_disponible.estado = 'ocupado'
            espacio_disponible.save()
            self.save()
            return True
        return False


class Salida(models.Model):
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)
    hora_salida = models.DateTimeField(auto_now_add=True)
    tiempo_total = models.IntegerField(null=True, blank=True)
    valor_pagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Salida {self.ingreso.placa}"

    def liberar_espacio(self):
        if self.ingreso.espacio:
            self.ingreso.espacio.estado = 'disponible'
            self.ingreso.espacio.save()


class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    placa = models.CharField(max_length=10)
    tipo_vehiculo = models.CharField(max_length=20)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20,
        default='activa'
    )
    def _str_(self):
        return self.placa


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    username = models.CharField(
        max_length=50,
        unique=True
    )
    password = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('empleado', 'Empleado')
        ]
    )
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre


class Configuracion(models.Model):
    capacidad_total = models.IntegerField()
    alerta_parqueadero_lleno = models.BooleanField(
        default=True
    )
    alerta_reserva_expirada = models.BooleanField(
        default=True
    )
    tiempo_maximo_horas = models.IntegerField()
    def _str_(self):
        return "Configuración"
