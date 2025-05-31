# Proyecto: TikNek_Viajes – Alcance funcional del MVP

## Objetivo general
El objetivo de este proyecto es desarrollar un MVP funcional para una empresa ficticia de viajes, donde los usuarios puedan consultar viajes, conocer los guías asignados y gestionar sus propios perfiles. Administradores podrán gestionar los viajes y los usuarios desde el panel Admin de Django.

## Roles

- **Usuario visitante**: No autenticado. Puede ver viajes, guías y página About.
- **Usuario registrado**: Puede ver y editar su perfil, con foto/avatar, y marcar interés en viajes.
- **Administrador**: Gestiona viajes, guías y pilotos desde el panel de administración de Django. También puede asignar usuarios a grupos y cambiar contraseñas.

---

## Funcionalidades principales

### 1. Viajes
- Ver listado de viajes planificados (filtros opcionales: destino, fecha, etc.)
- Ver detalle del viaje con:
  - Fecha, destino, descripción
  - Guía asignado
  - Pilotos inscriptos
- (Opcional para admins) **Soft delete** de viajes en lugar de borrado real.

### 2. Preinscripción
- Botón en cada viaje que abra el mail del usuario con subject prellenado:  
  `Asunto: Me interesa más información sobre el viaje X`

### 3. Guías
- Listado de guías
- Detalle de cada guía con su “CV” o experiencia

### 4. Usuarios
- Login, logout, registro
- Edición de perfil personal:
  - Nombre, email, agregar/cambiar foto/avatar
- Los administradores pueden:
  - Cambiar contraseñas desde el panel de administración
  - Asignar grupos a los usuarios

### 5. Página About
- Página estática con info general sobre la empresa

---

## Consideraciones técnicas

- Base de datos: SQLite
- Panel de administración: se usará el admin de Django para gestión de usuarios, grupos, viajes y asignaciones.
- Frameworks: Django + Bootstrap
- CRUD básico en frontend solo donde tenga sentido para el demo (por ejemplo, perfil personal)
- Imágenes de avatar y carga de CV: guardar localmente en `/media/` (no es necesario S3 ni servicios externos)
- Mensajes de confirmación (exito/error) en las acciones principales con `messages` de Django


## Tecnologías utilizadas

- Python 3.x
- Django 4.2.x
- SQLite3
- Bootstrap (vía CDN)
- HTML / CSS
- Django Widget Tweaks
- CKEditor v5 para texto enriquecido. Atención: requiere algunas configs extra que la v4 que tiene VULNs
- Pillow (para poder usar ImageField)

---

## Ideas para agregar si hay tiempo

- Validaciones custom en formularios
- Soft delete de viajes
- Fecha de creación/modificación de objetos
- Historial de cambios (nivel muy opcional, si sobra tiempo)