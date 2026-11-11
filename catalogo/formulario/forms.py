from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        max_length=20,
        label="Nombre de usuario",
        help_text="Máximo 20 caracteres.",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'maxlength': '20',
                'autocomplete': 'username',
            }
        ),
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data['email']
        dominio = email.rsplit('@', 1)[1]
        if len(dominio) < 4:
            raise forms.ValidationError(
                "La parte del correo después de @ debe tener al menos 4 caracteres."
            )
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        password_normalizada = password.casefold()

        datos_personales = (
            self.cleaned_data.get('first_name', ''),
            self.cleaned_data.get('last_name', ''),
        )
        for dato in datos_personales:
            if dato and password_normalizada == dato.strip().casefold():
                raise forms.ValidationError(
                    "La contraseña no puede ser igual a tu nombre o apellido."
                )

        errores = []
        if len(password) < 8:
            errores.append("tener al menos 8 caracteres")
        if not any(not caracter.isalnum() for caracter in password):
            errores.append("contener un carácter especial (por ejemplo: # o ,)")
        if not any(caracter.isdigit() for caracter in password):
            errores.append("contener un carácter numérico")
        if not any(caracter.isupper() for caracter in password):
            errores.append("contener una letra mayúscula")

        if errores:
            raise forms.ValidationError(
                "La contraseña debe " + ", ".join(errores) + "."
            )

        return password