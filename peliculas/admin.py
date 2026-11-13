from django.contrib import admin


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'anio_estreno', 'duracion_minutos', 'genero', 'clasificacion', 'disponible')
    list_filter = ('genero', 'clasificacion', 'disponible')
    search_fields = ('titulo', 'sinopsis')

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(PeliculaActor)
class PeliculaActorAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'actor', 'personaje', 'es_protagonista', 'orden_creditos')
    list_filter = ('es_protagonista',)
    search_fields = ('pelicula__titulo', 'actor__nombre', 'personaje')
    