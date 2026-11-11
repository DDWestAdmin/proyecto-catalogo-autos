from django.test import TestCase

from .forms import RegistroUsuarioForm


class RegistroUsuarioFormTests(TestCase):
    datos_base = {
        'username': 'usuario-prueba',
        'first_name': 'Ana',
        'last_name': 'García',
        'email': 'ana@example.com',
        'password2': 'Segura#123',
    }

    def datos_con_password(self, password):
        return {**self.datos_base, 'password1': password, 'password2': password}

    def test_acepta_password_que_cumple_todos_los_requisitos(self):
        formulario = RegistroUsuarioForm(
            data=self.datos_con_password('Segura#123')
        )

        self.assertTrue(formulario.is_valid())

    def test_acepta_nombre_de_usuario_de_20_caracteres(self):
        datos = self.datos_con_password('Segura#123')
        datos['username'] = 'u' * 20

        formulario = RegistroUsuarioForm(data=datos)

        self.assertTrue(formulario.is_valid())

    def test_rechaza_nombre_de_usuario_de_mas_de_20_caracteres(self):
        datos = self.datos_con_password('Segura#123')
        datos['username'] = 'u' * 21

        formulario = RegistroUsuarioForm(data=datos)

        self.assertFalse(formulario.is_valid())
        self.assertIn('username', formulario.errors)

    def test_acepta_correo_con_dominio_de_al_menos_4_caracteres(self):
        datos = self.datos_con_password('Segura#123')
        datos['email'] = 'ana@a.co'

        formulario = RegistroUsuarioForm(data=datos)

        self.assertTrue(formulario.is_valid())

    def test_rechaza_correo_con_dominio_demasiado_corto(self):
        datos = self.datos_con_password('Segura#123')
        datos['email'] = 'ana@a.c'

        formulario = RegistroUsuarioForm(data=datos)

        self.assertFalse(formulario.is_valid())
        self.assertIn('email', formulario.errors)

    def test_rechaza_correo_con_formato_invalido(self):
        datos = self.datos_con_password('Segura#123')
        datos['email'] = 'ana-correo-invalido'

        formulario = RegistroUsuarioForm(data=datos)

        self.assertFalse(formulario.is_valid())
        self.assertIn('email', formulario.errors)

    def test_rechaza_password_igual_al_nombre_o_apellido(self):
        for dato_personal in ('Ana', 'García'):
            with self.subTest(dato_personal=dato_personal):
                formulario = RegistroUsuarioForm(
                    data=self.datos_con_password(dato_personal)
                )

                self.assertFalse(formulario.is_valid())
                self.assertIn('nombre o apellido', formulario.errors['password1'][0])

    def test_rechaza_password_sin_longitud_minima(self):
        formulario = RegistroUsuarioForm(data=self.datos_con_password('Aa1#'))

        self.assertFalse(formulario.is_valid())
        self.assertIn('al menos 8 caracteres', formulario.errors['password1'][0])

    def test_rechaza_password_sin_caracter_especial(self):
        formulario = RegistroUsuarioForm(data=self.datos_con_password('Segura123'))

        self.assertFalse(formulario.is_valid())
        self.assertIn('carácter especial', formulario.errors['password1'][0])

    def test_rechaza_password_sin_numero(self):
        formulario = RegistroUsuarioForm(data=self.datos_con_password('Segura##'))

        self.assertFalse(formulario.is_valid())
        self.assertIn('carácter numérico', formulario.errors['password1'][0])

    def test_rechaza_password_sin_mayuscula(self):
        formulario = RegistroUsuarioForm(data=self.datos_con_password('segura#123'))

        self.assertFalse(formulario.is_valid())
        self.assertIn('letra mayúscula', formulario.errors['password1'][0])
