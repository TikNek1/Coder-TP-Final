# Proyecto: TikNek_Viajes – Alcance funcional del MVP

## Objetivo general
El objetivo de este proyecto es desarrollar un MVP funcional para una empresa ficticia de viajes, donde los usuarios puedan consultar viajes, conocer los guías asignados y gestionar sus propios perfiles. Administradores podrán gestionar los viajes y los usuarios desde el panel Admin de Django.

## Roles

- **Usuario visitante**: No autenticado. Puede ver viajes, guías y página About, puede registrarse.
- **Usuario registrado**: Puede ver viajes, guías, pilotos y editar su usuario/perfil, marcar interés en viajes.
- **Usuario Editor / grupo TikNek**: Gestiona viajes, guías y pilotos. Responde consultas vía chat
- **Administrador**: Gestiona viajes, guías y pilotos. Desde el panel de administración de Django, gestiona usuarios/grupos.

## Usuario/pw para pruebas

- **admin / coder123**: usuario con perfil administrador
- **info.viajes / coder123**: usuario con perfil editor. Importante tener este usuario, ya que es quien recibe los chats de los interesados a los viajes. Debe existir!

---

## Funcionalidades principales

### 1. Viajes
- Ver listado de viajes planificados (filtros opcionales: destino, fecha, etc.)
- Ver detalle del viaje con:
  - Fecha, destino, descripción
  - Guía asignado
  - Pilotos inscriptos
- (Opcional para admins) **Soft delete** de viajes en lugar de borrado real, quedan archivados o en borrador.

### 2. Interés / Consultas sobre un viaje
- Botón en cada viaje que abre un chat prellenado con el usuario info_viajes:  
  Asunto: 'Estoy interesado en el viaje X`

### 3. Usuarios
- Login, logout, registro
- Edición de "Mi Usuario":
  - Nombre/Apellido, email
- Edición de "Mi perfil":
  - Telefono, fecha nacimiento, ciudad, país, moto, datos personales, cambiar avatar
- Los administradores pueden desde /admin:
  - Asignar grupos a los usuarios
  - ABM de usuarios

### 4. Pilotos
- Lista de pilotos
- Detalle de pilotos
- Chat con un piloto
- (Admin / Editor) Edición/Eliminación de perfil de piloto


### 5. Guías
- Listado / detalle de cada guía con su “CV” o experiencia
- (Admin / Editor) Edición/Eliminación de perfil de piloto


### 6. Página About
- Página estática con info general sobre la empresa

### 7. Messages APP / Chat
- Permite el chat 1:1 entre los usuarios autenticados en la plataforma
- Cada usuario puede seleccionar a quién enviarle un mensaje, como así también ver respuestas e histórico
- La app se usa también para que el usuario info.viajes responda preguntas de interesados a un viaje

---

## Consideraciones técnicas

- Base de datos: SQLite
- Panel de administración: se usará el admin de Django para gestión de usuarios, grupos, viajes y asignaciones.
- Frameworks: Django + Bootstrap
- CRUD básico en frontend solo donde tenga sentido para el demo (por ejemplo, piloto, guia, viajes)
- Imágenes de avatar: guardar localmente en `/static/`
- Mensajes de confirmación (exito/error) en las acciones principales con `messages` de Django


## Tecnologías utilizadas

- Python 3.x
- Django 4.2.x
- SQLite3
- Bootstrap (vía CDN)
- HTML / CSS
- Django Widget Tweaks
- Pillow (para poder usar ImageField)
- Faker (para popular la BD con datos ficticios)

---
