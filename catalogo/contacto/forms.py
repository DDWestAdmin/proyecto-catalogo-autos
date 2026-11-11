from django import forms

class ContactoForm(forms.Form):
    nombre_completo = forms.CharField(
        max_length=150,
        label="Nombre completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre completo'})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    fono = forms.CharField(
        max_length=20,
        label="Fono",
        widget=forms.TelInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'})
    )
    asunto = forms.CharField(
        max_length=100,
        label="Asunto de la Consulta",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Consulta sobre financiamiento'})
    )