from faker import Faker
import random
from django.contrib.auth.models import User
from viajes.models import Guia, Piloto, Viaje
from datetime import date, timedelta



"""
--------------------------------------------------------------------------------------------------------------------------------
Limpieza de datos existentes

ATENCION, no se eliminan los usuarios de la tabla user, solo los modelos específicos 
Para eliminar usuarios, hacerlos desde consola /admin, cuidado de no borrar el usuario "admin" ni los usuarios del grupo TikNek
Para encontrarlos fácil, ordenar por el campo "Staff status" en la tabla de usuarios del admin de Django

Para ejecutar este script, usar el comando:
python manage.py shell < cargar_datos_fake.py

--------------------------------------------------------------------------------------------------------------------------------
"""
# Limpieza de datos existentes
Guia.objects.all().delete()
Piloto.objects.all().delete()
Viaje.objects.all().delete()


fake = Faker('es_AR')

# --- Crear Guías ---
guias = []
for _ in range(4):
    guia = Guia.objects.create(
        nombre=fake.first_name(),
        apellido=fake.last_name(),
        email=fake.email(),
        dni=fake.unique.random_number(digits=8),
        telefono=fake.phone_number(),
        fecha_nac=fake.date_of_birth(minimum_age=25, maximum_age=60),
        ciudad=fake.city(),
        pais=random.choice(['AR', 'BR', 'CL']),
        sobre_mi=fake.paragraph(nb_sentences=5),
    )
    guias.append(guia)

# --- Crear Pilotos y Users ---
pilotos = []
for _ in range(25):
    first_name = fake.first_name()
    last_name = fake.last_name()
    user = User.objects.create_user(
        username=fake.unique.user_name(),
        first_name=first_name,
        last_name=last_name,
        email=fake.email(),
        password='test1234'
    )
    piloto = Piloto.objects.create(
        user=user,
        telefono=fake.phone_number(),
        fecha_nac=fake.date_of_birth(minimum_age=20, maximum_age=55),
        ciudad=fake.city(),
        pais=random.choice(['AR', 'BR', 'CL']),
        sobre_mi=fake.text(max_nb_chars=200),
        moto=random.choice(['KTM 890', 'Yamaha Tenere', 'Honda Tornado', 'BMW GS 1250']),
    )
    pilotos.append(piloto)

# Crear viajes


start_date = date.today() + timedelta(days=1)
end_date = date.today() + timedelta(days=180)

for _ in range(20):
    guia = random.choice(guias)
    fecha_salida = fake.date_between(start_date=start_date, end_date=end_date)

    viaje = Viaje.objects.create(
        nombre=f"{fake.word().capitalize()} Trip",
        detalle=fake.paragraph(nb_sentences=10),
        fecha_salida=fecha_salida,
        cant_dias=random.randint(3, 10),
        km=random.randint(300, 1500),
        dificultad=random.choice(['baja', 'media', 'alta']),
        guia=guia,
        activo=random.choice([True, True, False]),
        max_pilotos=random.randint(5, 15)
    )

    # Asignar entre 1 y N pilotos (respetando max_pilotos)
    cantidad = random.randint(1, viaje.max_pilotos)
    pilotos_asignados = random.sample(pilotos, k=min(cantidad, len(pilotos)))
    viaje.pilotos.add(*pilotos_asignados)