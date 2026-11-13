from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    anio_estreno = models.IntegerField()
    duracion_minutos = models.IntegerField()
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE)
    clasificacion = models.CharField(max_length=2)
    sinopsis = models.TextField()
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} ({self.anio_estreno})'


class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class PeliculaActor(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    actor = models.ForeignKey('Actor', on_delete=models.CASCADE)
    personaje = models.CharField(max_length=150)
    es_protagonista = models.BooleanField(default=True)
    orden_creditos = models.IntegerField(default=1)

    class Meta:
        ordering = ('orden_creditos', 'id')

    def __str__(self):
        return f'{self.actor} - {self.pelicula}'


class Actor(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=60)
    biografia = models.TextField()
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre