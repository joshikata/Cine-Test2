import datetime

from django.db import migrations, models
import django.db.models.deletion


def crear_catalogo_inicial(apps, schema_editor):
    Genero = apps.get_model('peliculas', 'Genero')
    Pelicula = apps.get_model('peliculas', 'Pelicula')
    Actor = apps.get_model('peliculas', 'Actor')
    PeliculaActor = apps.get_model('peliculas', 'PeliculaActor')

    generos = {}
    for nombre, descripcion in (
        ('Drama', 'Historias centradas en sus personajes y sus decisiones.'),
        ('Suspenso', 'Relatos de misterio, tensión y giros inesperados.'),
        ('Ciencia ficción', 'Mundos imaginados y futuros posibles.'),
        ('Aventura', 'Viajes, descubrimientos y grandes desafíos.'),
        ('Crimen', 'Historias sobre poder, lealtad y el mundo criminal.'),
    ):
        generos[nombre], _ = Genero.objects.using(schema_editor.connection.alias).get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'activo': True},
        )

    catalogo = (
        {
            'titulo': 'Casablanca',
            'anio': 1942,
            'duracion': 102,
            'genero': 'Drama',
            'clasificacion': 'PG',
            'sinopsis': 'En una ciudad marcada por la guerra, un antiguo amor vuelve a cruzarse con un dueño de café.',
            'actores': (
                ('Humphrey Bogart', '1899-12-25', 'Estadounidense', 'Rick Blaine, dueño de un café en Casablanca.'),
                ('Ingrid Bergman', '1915-08-29', 'Sueca', 'Ilsa Lund, cuyo pasado vuelve a encontrarse con Rick.'),
            ),
        },
        {
            'titulo': 'La ventana indiscreta',
            'anio': 1954,
            'duracion': 112,
            'genero': 'Suspenso',
            'clasificacion': 'PG',
            'sinopsis': 'Un fotógrafo convaleciente observa a sus vecinos y empieza a sospechar que ocurrió un crimen.',
            'actores': (
                ('James Stewart', '1908-05-20', 'Estadounidense', 'L. B. Jefferies, fotógrafo en recuperación.'),
                ('Grace Kelly', '1929-11-12', 'Estadounidense', 'Lisa Fremont, pareja de Jefferies.'),
            ),
        },
        {
            'titulo': 'El padrino',
            'anio': 1972,
            'duracion': 175,
            'genero': 'Crimen',
            'clasificacion': 'R',
            'sinopsis': 'La familia Corleone enfrenta un cambio de poder que transforma el destino de sus integrantes.',
            'actores': (
                ('Marlon Brando', '1924-04-03', 'Estadounidense', 'Vito Corleone, patriarca de la familia.'),
                ('Al Pacino', '1940-04-25', 'Estadounidense', 'Michael Corleone, el hijo menor de Vito.'),
            ),
        },
        {
            'titulo': 'Volver al futuro',
            'anio': 1985,
            'duracion': 116,
            'genero': 'Aventura',
            'clasificacion': 'PG',
            'sinopsis': 'Un adolescente viaja accidentalmente al pasado y debe encontrar el camino de regreso a casa.',
            'actores': (
                ('Michael J. Fox', '1961-06-09', 'Canadiense', 'Marty McFly, un joven que viaja en el tiempo.'),
                ('Christopher Lloyd', '1938-10-22', 'Estadounidense', 'Emmett Brown, inventor de la máquina del tiempo.'),
            ),
        },
        {
            'titulo': 'Matrix',
            'anio': 1999,
            'duracion': 136,
            'genero': 'Ciencia ficción',
            'clasificacion': 'R',
            'sinopsis': 'Un programador descubre que la realidad cotidiana esconde una verdad extraordinaria.',
            'actores': (
                ('Keanu Reeves', '1964-09-02', 'Canadiense', 'Neo, un programador que busca respuestas.'),
                ('Carrie-Anne Moss', '1967-08-21', 'Canadiense', 'Trinity, una aliada clave en la resistencia.'),
            ),
        },
    )

    for item in catalogo:
        pelicula, _ = Pelicula.objects.using(schema_editor.connection.alias).get_or_create(
            titulo=item['titulo'],
            defaults={
                'anio_estreno': item['anio'],
                'duracion_minutos': item['duracion'],
                'genero': generos[item['genero']],
                'clasificacion': item['clasificacion'],
                'sinopsis': item['sinopsis'],
                'disponible': True,
            },
        )
        for orden, (nombre, nacimiento, nacionalidad, personaje) in enumerate(item['actores'], start=1):
            actor, _ = Actor.objects.using(schema_editor.connection.alias).get_or_create(
                nombre=nombre,
                defaults={
                    'fecha_nacimiento': datetime.date.fromisoformat(nacimiento),
                    'nacionalidad': nacionalidad,
                    'biografia': personaje,
                    'activo': True,
                },
            )
            PeliculaActor.objects.using(schema_editor.connection.alias).get_or_create(
                pelicula=pelicula,
                actor=actor,
                defaults={
                    'personaje': personaje,
                    'es_protagonista': True,
                    'orden_creditos': orden,
                },
            )


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pelicula',
            name='anio_estreno',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=60)),
                ('biografia', models.TextField()),
                ('activo', models.BooleanField(default=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeliculaActor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personaje', models.CharField(max_length=150)),
                ('es_protagonista', models.BooleanField(default=True)),
                ('orden_creditos', models.IntegerField(default=1)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peliculas.actor')),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='peliculas.pelicula')),
            ],
            options={
                'ordering': ('orden_creditos', 'id'),
            },
        ),
        migrations.RunPython(crear_catalogo_inicial, migrations.RunPython.noop),
    ]
