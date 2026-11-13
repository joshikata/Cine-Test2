from django.shortcuts import render

from .models import Actor, Pelicula


def lista_peliculas(request):
    peliculas = (
        Pelicula.objects.select_related('genero')
        .prefetch_related('peliculaactor_set__actor')
        .order_by('-anio_estreno', 'titulo')
    )
    return render(
        request,
        'peliculas/lista.html',
        {
            'peliculas': peliculas,
            'total_peliculas': peliculas.count(),
            'total_actores': Actor.objects.count(),
        },
    )
