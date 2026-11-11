import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import ANIO_CHOICES, VehiculoForm
from .models import Vehiculo


class PermisosCatalogoTests(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(
            modelo='Ford Bronco',
            anio=2020,
            descripcion='Vehículo de prueba',
        )
        self.usuario = User.objects.create_user(
            username='usuario',
            password='Contrasena#123',
        )
        self.administrador = User.objects.create_user(
            username='administrador',
            password='Contrasena#123',
            is_staff=True,
        )

    def test_usuario_registrado_puede_crear_vehiculos(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse('crear_vehiculo'),
            {'modelo': 'Toyota Corolla', 'anio': 2021},
        )

        self.assertEqual(respuesta.status_code, 302)
        vehiculo = Vehiculo.objects.get(modelo='Toyota Corolla')
        self.assertEqual(vehiculo.propietario, self.usuario)

    def test_usuario_registrado_no_puede_editar_vehiculo_de_otro_usuario(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse('editar_vehiculo', args=[self.vehiculo.id]),
            {'modelo': 'Modelo no autorizado', 'anio': 2022},
        )

        self.assertEqual(respuesta.status_code, 302)
        self.vehiculo.refresh_from_db()
        self.assertEqual(self.vehiculo.modelo, 'Ford Bronco')

    def test_usuario_registrado_no_puede_eliminar_vehiculo_de_otro_usuario(self):
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse('eliminar_vehiculo', args=[self.vehiculo.id]),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Vehiculo.objects.filter(id=self.vehiculo.id).exists())

    def test_usuario_registrado_puede_editar_vehiculo_propio(self):
        self.vehiculo.propietario = self.usuario
        self.vehiculo.save(update_fields=['propietario'])
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse('editar_vehiculo', args=[self.vehiculo.id]),
            {'modelo': 'Ford Bronco actualizado', 'anio': 2022},
        )

        self.assertEqual(respuesta.status_code, 302)
        self.vehiculo.refresh_from_db()
        self.assertEqual(self.vehiculo.modelo, 'Ford Bronco actualizado')

    def test_usuario_registrado_puede_eliminar_vehiculo_propio(self):
        self.vehiculo.propietario = self.usuario
        self.vehiculo.save(update_fields=['propietario'])
        self.client.force_login(self.usuario)

        respuesta = self.client.post(
            reverse('eliminar_vehiculo', args=[self.vehiculo.id]),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Vehiculo.objects.filter(id=self.vehiculo.id).exists())

    def test_administrador_puede_crear_vehiculos(self):
        self.client.force_login(self.administrador)

        respuesta = self.client.post(
            reverse('crear_vehiculo'),
            {'modelo': 'Toyota Corolla', 'anio': 2021},
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Vehiculo.objects.filter(modelo='Toyota Corolla').exists())

    def test_administrador_puede_eliminar_vehiculo_de_otro_usuario(self):
        self.vehiculo.propietario = self.usuario
        self.vehiculo.save(update_fields=['propietario'])
        self.client.force_login(self.administrador)

        respuesta = self.client.post(
            reverse('eliminar_vehiculo', args=[self.vehiculo.id]),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Vehiculo.objects.filter(id=self.vehiculo.id).exists())

    def test_administrador_puede_editar_vehiculos(self):
        self.client.force_login(self.administrador)

        respuesta = self.client.post(
            reverse('editar_vehiculo', args=[self.vehiculo.id]),
            {'modelo': 'Ford Bronco actualizado', 'anio': 2022},
        )

        self.assertEqual(respuesta.status_code, 302)
        self.vehiculo.refresh_from_db()
        self.assertEqual(self.vehiculo.modelo, 'Ford Bronco actualizado')

    def test_administrador_puede_eliminar_vehiculos(self):
        self.client.force_login(self.administrador)

        respuesta = self.client.post(
            reverse('eliminar_vehiculo', args=[self.vehiculo.id]),
        )

        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Vehiculo.objects.filter(id=self.vehiculo.id).exists())


class ImagenesVehiculoTests(TestCase):
    def test_la_ruta_de_imagen_incluye_la_carpeta_de_autos(self):
        imagen = SimpleUploadedFile(
            'Ford Bronco.jpg',
            b'contenido-de-prueba',
            content_type='image/jpeg',
        )

        vehiculo = Vehiculo.objects.create(
            modelo='Ford Bronco',
            anio=2020,
            foto=imagen,
        )

        self.assertTrue(vehiculo.foto.name.startswith('autos/'))
        self.assertTrue(vehiculo.foto.name.endswith('.jpg'))
        vehiculo.foto.delete(save=False)


class AnioVehiculoFormTests(TestCase):
    def test_anio_se_muestra_como_lista_desde_1930_hasta_2026(self):
        formulario = VehiculoForm()

        self.assertIsInstance(formulario.fields['anio'].widget, forms.Select)
        self.assertEqual(ANIO_CHOICES[0], (1930, '1930'))
        self.assertEqual(ANIO_CHOICES[-1], (2026, '2026'))
        self.assertEqual(len(ANIO_CHOICES), 97)

    def test_formulario_rechaza_anios_fuera_del_rango(self):
        formulario = VehiculoForm(data={'modelo': 'Vehículo', 'anio': 1929})

        self.assertFalse(formulario.is_valid())
        self.assertIn('anio', formulario.errors)


class DescripcionVehiculoFormTests(TestCase):
    def test_descripcion_tiene_limite_de_100_caracteres(self):
        formulario = VehiculoForm()

        self.assertEqual(formulario.fields['descripcion'].max_length, 100)
        self.assertEqual(formulario.fields['descripcion'].widget.attrs['maxlength'], '100')

    def test_formulario_rechaza_descripcion_de_mas_de_100_caracteres(self):
        formulario = VehiculoForm(
            data={
                'modelo': 'Vehículo',
                'anio': 2020,
                'descripcion': 'x' * 101,
            }
        )

        self.assertFalse(formulario.is_valid())
        self.assertIn('descripcion', formulario.errors)

    def test_el_catalogo_renderiza_la_imagen_del_vehiculo(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                imagen = SimpleUploadedFile(
                    'ford-bronco.jpg',
                    b'contenido-de-prueba',
                    content_type='image/jpeg',
                )
                vehiculo = Vehiculo.objects.create(
                    modelo='Ford Bronco',
                    anio=2020,
                    foto=imagen,
                )

                respuesta = self.client.get(reverse('catalogo_autos'))

                self.assertEqual(respuesta.status_code, 200)
                self.assertContains(respuesta, vehiculo.foto.url)
                self.assertContains(respuesta, 'alt="Ford Bronco"')
                vehiculo.foto.delete(save=False)
