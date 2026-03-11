from django.contrib import admin
from django.urls import path
from parqueadero import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar/', views.registrar_vehiculo, name='registrar'),
]