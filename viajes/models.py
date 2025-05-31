from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field # para manejar contenido enriquecido con la v5

class Guia(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, choices=[
        ('AR', 'Argentina'), 
        ('BR', 'Brasil'), 
        ('CL', 'Chile'), 
        ('OT', 'Otro')
    ])  
    # despues ver si agrego mas paises o relaciono con tabla de paises
    sobre_mi = CKEditor5Field("Sobre mí", config_name="default")
    foto = models.ImageField(upload_to='guias_fotos/', null=True, blank=True)
    # OJO: Para ImageField tener configurado MEDIA_ROOT y MEDIA_URL en settings.py, 
    # y agregar urlpatterns en urls.py para servir archivos en desarrollo.

    def __str__(self):
        return f"Guía: {self.user.get_full_name()}"


class Piloto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, choices=[
        ('AR', 'Argentina'), 
        ('BR', 'Brasil'), 
        ('CL', 'Chile'), 
        ('OT', 'Otro')
    ])  
    # despues ver si agrego mas paises o relaciono con tabla de paises
    sobre_mi = CKEditor5Field("Sobre mí", config_name="default")
    moto = models.CharField(max_length=100, default="Sin, por ahora")
    avatar = models.ImageField(upload_to='pilotos_avatars/', null=True, blank=True)

    def __str__(self):
        return f"Piloto: {self.user.get_full_name()}"


class Viaje(models.Model):
    DIFICULTAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    nombre = models.CharField(max_length=100)
    detalle = CKEditor5Field("detalle", config_name="default")
    fecha_salida = models.DateField()
    cant_dias = models.PositiveIntegerField()
    km = models.PositiveIntegerField()
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES)
    guia = models.ForeignKey(Guia, null=True, blank=True, on_delete=models.SET_NULL)
    pilotos = models.ManyToManyField(Piloto, blank=True)
    activo = models.BooleanField(default=True)
    max_pilotos = models.PositiveIntegerField()
    fecha_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.fecha_salida})"