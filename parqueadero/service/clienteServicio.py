from django.db.models import Count
from django.http import HttpRequest
from parqueadero.models import Ingreso, Salida


class ClienteServicio:

    def historial(self, request: HttpRequest):

        buscar = request.GET.get('buscar')

        ingresos = Ingreso.objects.all().order_by('-hora_ingreso')
        salidas = Salida.objects.all().order_by('-hora_salida')

        resultados = None

        if buscar:
            ingreso = Ingreso.objects.filter(
                placa__icontains=buscar
            ).order_by('-hora_ingreso').first()

            salida = Salida.objects.filter(
                ingreso__placa__icontains=buscar
            ).order_by('-hora_salida').first()

            resultados = {
                'ingresos': ingreso,
                'salidas': salida
            }

        frecuentes = (
            Ingreso.objects
            .values('placa')
            .annotate(total=Count('placa'))
            .order_by('-total')[:5]
        )

        return {
            'ingresos': ingresos,
            'salidas': salidas,
            'frecuentes': frecuentes,
            'resultados': resultados,
            'buscar': buscar
        }
