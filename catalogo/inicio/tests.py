from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse


class DisenoPaginaTests(TestCase):
    def test_inicio_conserva_los_bloques_visuales_principales(self):
        respuesta = self.client.get(reverse('inicio'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'home-page')
        self.assertContains(respuesta, 'home-banner')
        self.assertContains(respuesta, 'carouselVehiculos')
        self.assertContains(respuesta, 'catalogue-callout')
        self.assertContains(respuesta, 'carousel-empty')

    def test_catalogo_conserva_tarjetas_y_acciones_visuales(self):
        respuesta = self.client.get(reverse('catalogo_autos'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Catálogo de Vehículos')
        self.assertContains(respuesta, 'Debe Registrarse para poder añadir vehículos.')

    def test_css_contiene_reglas_de_diseno_responsive(self):
        css_path = Path(settings.STATIC_DIR) / 'styles.css'
        css = css_path.read_text(encoding='utf-8')

        for selector in (
            '.vehicle-image',
            '.home-banner',
            '.home-carousel-section #carouselVehiculos',
            '.catalogue-callout',
            '@media (max-width: 576px)',
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, css)
