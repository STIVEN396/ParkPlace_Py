from django.shortcuts import render, redirect
from .forms import VehiculoForm

def registrar_vehiculo(request):

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar')

    else:
        form = VehiculoForm()

    return render(request, 'registrar.html', {'form': form})