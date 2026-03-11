from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VehiculoForm


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def registrar_vehiculo(request):

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = VehiculoForm()

    return render(request, 'registrar.html', {'form': form})