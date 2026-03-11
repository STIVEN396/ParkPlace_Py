from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)
    tipo = models.CharField(max_length=20)
    hora_ingreso = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.placa