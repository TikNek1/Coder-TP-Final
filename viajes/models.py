from django.db import models
from django.contrib.auth.models import User

class Guia(models.Model):
    """
    Modelo que representa un guía de viaje.

    Campos:
    - nombre: Nombre del guía (máximo 100 caracteres).
    - apellido: Apellido del guía (máximo 100 caracteres).
    - email: Correo electrónico del guía.
    - dni: Documento Nacional de Identidad del guía (único).
    - telefono: Número de teléfono del guía.
    - fecha_nac: Fecha de nacimiento del guía (opcional).
    - ciudad: Ciudad de residencia del guía.
    - pais: País de residencia del guía (opciones predefinidas).
    - sobre_mi: Descripción personal del guía (opcional).
    - foto: Foto del guía (opcional, almacenada en la carpeta 'guias_fotos/').

    Notas:
    - Para el campo `foto`, es necesario configurar `MEDIA_ROOT` y `MEDIA_URL` en `settings.py`.
    - En desarrollo, se deben agregar `urlpatterns` para servir archivos estáticos.

    Métodos:
    - __str__: Devuelve una representación en texto del guía (nombre y apellido).
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    fecha_nac = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, choices=[
        ('AR', 'Argentina'), 
        ('BR', 'Brasil'), 
        ('CL', 'Chile'), 
        ('OT', 'Otro')
    ])
    sobre_mi = models.TextField(blank=True)
    foto = models.ImageField(upload_to='guias_fotos/', null=True, blank=True)

    def __str__(self):
        return f"Guía: {self.nombre} {self.apellido}"


class Piloto(models.Model):
    """
    Modelo que representa un piloto.

    Campos:
    - user: Relación uno a uno con el modelo `User` de Django.
    - telefono: Número de teléfono del piloto.
    - fecha_nac: Fecha de nacimiento del piloto (opcional).
    - ciudad: Ciudad de residencia del piloto.
    - pais: País de residencia del piloto (opciones predefinidas).
    - sobre_mi: Descripción personal del piloto (opcional).
    - moto: Modelo o descripción de la moto del piloto (opcional, valor por defecto: "Sin, por ahora").
    - avatar: Nombre del archivo del avatar del piloto (valor por defecto: 'default.png').

    Métodos:
    - __str__: Devuelve una representación en texto del piloto (nombre completo del usuario asociado).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    fecha_nac = models.DateField(null=True, blank=True)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, choices=[
        ('AR', 'Argentina'), 
        ('BR', 'Brasil'), 
        ('CL', 'Chile'), 
        ('OT', 'Otro')
    ])
    sobre_mi = models.TextField(blank=True)
    moto = models.CharField(max_length=100, default="Sin, por ahora", blank=True)
    avatar = models.CharField(max_length=100, default='default.png')

    def __str__(self):
        return f"Piloto: {self.user.get_full_name()}"


class Viaje(models.Model):
    """
    Modelo que representa un viaje.

    Campos:
    - nombre: Nombre del viaje.
    - detalle: Descripción detallada del viaje.
    - fecha_salida: Fecha de salida del viaje.
    - cant_dias: Cantidad de días que dura el viaje.
    - km: Distancia total del viaje en kilómetros.
    - dificultad: Nivel de dificultad del viaje (opciones: baja, media, alta).
    - guia: Relación con el modelo `Guia` (opcional, se elimina la relación si el guía es eliminado).
    - pilotos: Relación muchos a muchos con el modelo `Piloto` (opcional).
    - activo: Indica si el viaje está activo o en estado de borrador.
    - max_pilotos: Número máximo de pilotos permitidos en el viaje.
    - fecha_update: Fecha y hora de la última actualización del viaje (se actualiza automáticamente).

    Métodos:
    - __str__: Devuelve una representación en texto del viaje (nombre y fecha de salida).
    """
    DIFICULTAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    nombre = models.CharField(max_length=100)
    detalle = models.TextField()
    fecha_salida = models.DateField()
    cant_dias = models.PositiveIntegerField()
    km = models.PositiveIntegerField()
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES)
    guia = models.ForeignKey(Guia, null=True, blank=True, on_delete=models.SET_NULL, related_name='viajes')
    pilotos = models.ManyToManyField(Piloto, blank=True, related_name='viajes')
    activo = models.BooleanField(default=True)
    max_pilotos = models.PositiveIntegerField()
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.fecha_salida})"