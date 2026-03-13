from django.contrib import admin
from .models import Espacio, Tarifa, Ingreso, Salida, Reserva, Usuario, Configuracion

admin.site.register(Espacio)
admin.site.register(Tarifa)
admin.site.register(Ingreso)
admin.site.register(Salida)
admin.site.register(Reserva)
admin.site.register(Usuario)
admin.site.register(Configuracion)