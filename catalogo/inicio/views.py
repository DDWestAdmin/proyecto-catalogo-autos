from django.shortcuts import render
from autos.models import Vehiculo

def inicio(request):
    vehiculos = Vehiculo.objects.exclude(foto__isnull=True).exclude(foto='')
    return render(request, 'inicio.html', {'vehiculos': vehiculos})