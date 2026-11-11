from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'anio', 'propietario')
    search_fields = ('modelo', 'descripcion')
    list_filter = ('anio', 'propietario')
