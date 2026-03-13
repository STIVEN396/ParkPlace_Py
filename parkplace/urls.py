from django.contrib import admin
from django.urls import path, include
from parqueadero import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('registrar/', views.registrar_vehiculo, name='registrar'),
    path("salida/", views.salida, name="salida"),

    path('accounts/', include('django.contrib.auth.urls')),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('registrar/', views.vehiculos, name='registrar'),

    path('vehiculos/', views.vehiculos, name='vehiculos'),

    path('historial/', views.historial, name='historial'),

    path('reportes/', views.reportes, name='reportes'),

    path('configuracion/', views.configuracion, name='configuracion'),

    path('mod7/', views.modulo7, name='mod7'),
    path('mod8/', views.modulo8, name='mod8'),
    path('mod9/', views.modulo9, name='mod9'),
    path('mod10/', views.modulo10, name='mod10'),

]