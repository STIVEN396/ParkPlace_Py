from django.contrib import admin
from django.urls import path, include
from parqueadero import views

urlpatterns = [

    path('', views.login, name='login'),
    
    path('admin/', admin.site.urls),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('registrar/', views.registrar_vehiculo, name='registrar'),
   
    path("salida/", views.salida, name="salida"),

    path('historial/', views.historial, name='historial'),

    path('reservas/', views.dashboard, name='reservas'),

    path('espacios/', views.dashboard, name='espacios'),

    path('tarifas/', views.dashboard, name='tarifas'),

    path('usuarios/', views.dashboard, name='usuarios'),

    path('reportes/', views.reportes, name='reportes'),

    path('configuracion/', views.configuracion, name='configuracion'),

    path('accounts/', include('django.contrib.auth.urls')),

    

]