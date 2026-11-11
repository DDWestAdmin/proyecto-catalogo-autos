import os
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

def ruta_foto_auto(instance, filename):
    # Genera la ruta dentro de media/autos/
    ext = os.path.splitext(filename)[1]
    nombre = "{}_{}{}".format(
        instance.modelo.replace(" ", "_").lower(), 
        timezone.now().strftime("%Y%m%d%H%M%S"), 
        ext
    )
    return os.path.join('autos', nombre)

class Vehiculo(models.Model):
    propietario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vehiculos_creados',
        verbose_name='Propietario',
    )
    modelo = models.CharField(max_length=100, verbose_name="Nombre del Modelo")
    anio = models.IntegerField(verbose_name="Año del Vehículo")
    descripcion = models.TextField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name="Descripción",
    )
    foto = models.ImageField(upload_to=ruta_foto_auto, null=True, blank=True, verbose_name="Fotografía")

    def __str__(self):
        return f"{self.modelo} ({self.anio})"

    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['modelo', 'anio']