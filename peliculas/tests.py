from django.test import TestCase
from django.urls import reverse

from .models import Actor, Genero, Pelicula, PeliculaActor


class CatalogoTests(TestCase):
    def test_catalogo_muestra_pelicula_y_reparto(self):
        genero = Genero.objects.create(nombre='Drama de prueba', descripcion='Historias de personajes.')
        pelicula = Pelicula.objects.create(
            titulo='Película de prueba',
            anio_estreno=2024,
            duracion_minutos=100,
            genero=genero,
            clasificacion='PG',
            sinopsis='Una historia breve.',
        )
        actor = Actor.objects.create(
            nombre='Actor de prueba',
            fecha_nacimiento='1990-01-01',
            nacionalidad='Chilena',
            biografia='Actor ficticio para una prueba.',
        )
        PeliculaActor.objects.create(
            pelicula=pelicula,
            actor=actor,
            personaje='Protagonista',
            orden_creditos=1,
        )

        response = self.client.get(reverse('peliculas'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Película de prueba')
        self.assertContains(response, 'Actor de prueba')
        self.assertTemplateUsed(response, 'peliculas/lista.html')

    def test_raiz_redirige_al_catalogo(self):
        response = self.client.get('/')

        self.assertRedirects(response, reverse('peliculas'))
