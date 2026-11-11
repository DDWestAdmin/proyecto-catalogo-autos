from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehiculo
from .forms import ANIO_CHOICES, VehiculoForm

# Lectura pública
def catalogo_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    form = VehiculoForm()
    return render(
        request,
        'catalogo.html',
        {'vehiculos': vehiculos, 'form': form, 'anios': ANIO_CHOICES},
    )

def puede_gestionar_vehiculo(user, vehiculo):
    return user.is_staff or vehiculo.propietario_id == user.id


@login_required
def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.propietario = request.user
            vehiculo.save()
            messages.success(request, "Vehículo registrado exitosamente.")
        else:
            messages.error(request, "Error al guardar el vehículo. Revisa los datos.")
    return redirect('catalogo_autos')

@login_required
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    if not puede_gestionar_vehiculo(request.user, vehiculo):
        messages.error(request, "No tienes permiso para editar este vehículo.")
        return redirect('catalogo_autos')

    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente.")
        else:
            messages.error(request, "No se pudo actualizar el vehículo.")
    return redirect('catalogo_autos')

@login_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    if not puede_gestionar_vehiculo(request.user, vehiculo):
        messages.error(request, "No tienes permiso para eliminar este vehículo.")
        return redirect('catalogo_autos')

    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado con éxito.")
    return redirect('catalogo_autos')