from django import forms
from .models import Vehiculo

ANIO_CHOICES = [(anio, str(anio)) for anio in range(1930, 2027)]


class VehiculoForm(forms.ModelForm):
    anio = forms.TypedChoiceField(
        choices=ANIO_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Vehiculo
        fields = ['modelo', 'anio', 'descripcion', 'foto']
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ford Bronco'}),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2,
                    'maxlength': 100,
                    'placeholder': 'Descripción corta del vehículo (máximo 100 caracteres)',
                }
            ),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }