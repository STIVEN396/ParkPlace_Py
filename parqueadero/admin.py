from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Espacio, Tarifa, Ingreso, Salida, Reserva, Usuario, Configuracion

admin.site.register(Espacio)
admin.site.register(Tarifa)
admin.site.register(Ingreso)
admin.site.register(Salida)
admin.site.register(Reserva)
admin.site.register(Configuracion)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
