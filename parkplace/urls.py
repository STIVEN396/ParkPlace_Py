from django.contrib import admin
from django.urls import path, include
from parqueadero import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar/', views.registrar_vehiculo, name='registrar'),
]