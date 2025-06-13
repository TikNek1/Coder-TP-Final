# Proyecto: TikNek Viajes

**Trabajo Final para el curso Python Flex en CoderHouse**
- Comisión: **69550**
- Alumno: **Nicolás Tecco**

## Tabla de Contenidos
- [Objetivo general](#objetivo-general)
- [Video explicativo](#video-explicativo)
- [Casos de test](#casos-de-test)
- [Roles](#roles)
- [Usuario/pw para pruebas](#usuariopw-para-pruebas)
- [Funcionalidades principales](#funcionalidades-principales)
- [Consideraciones técnicas](#consideraciones-técnicas)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Estructura de la Aplicación](#estructura-de-la-aplicación)
- [Instalación y ejecución de TikNek_Viajes](#instalación-y-ejecución-de-tiknek_viajes)

## Objetivo general
El objetivo de este proyecto es desarrollar un MVP funcional para una empresa ficticia de viajes, donde los usuarios puedan consultar viajes, conocer los guías asignados, gestionar sus propios perfiles y contactarse con otros pilotos. Administradores y Editores podrán gestionar los viajes, guías y pilotos.

---

## Video explicativo
[Ver en YouTube](https://youtu.be/YgW0i65BJqg) – Este video muestra el funcionamiento general del proyecto, cómo usarlo, diferentes roles, etc

## Casos de test
A modo de ejemplo, se presentan algunos casos de prueba relevantes. Se puede ver y bajar desde el mismo repo del proyecto: https://github.com/TikNek1/Coder-TP-Final-Tecco/blob/main/Casos%20de%20Test.xlsx. El documento fue realizado con MS Excel 365

---

## Roles

| Rol                | Permisos principales                                                                 |
|--------------------|--------------------------------------------------------------------------------------|
| Visitante  | Ver viajes, guías, página About, registrarse                                        |
| Usuario Registrado | Ver viajes, guías, pilotos, editar perfil, hacer consultas sobre viajes, contactar pilotos                        |
| Editor     | Gestionar viajes, guías, pilotos, responder consultas                               |
| Administrador      | Gestionar viajes, guías, pilotos. Usuarios y grupos desde el panel de administración |

## Usuario/pw para pruebas
- **admin / coder123**: usuario con perfil administrador
- **info.viajes / coder123**: usuario con perfil editor. Importante tener este usuario, ya que es quien recibe los chats de los interesados a los viajes. Debe existir!
- **Obs.** Hay varios usuarios creados con un script usando faker en la BD de test, todos tienen la contraseña **test1234**

---

## Funcionalidades principales

### 1. Viajes
- Ver listado de viajes planificados (filtros: destino/nombre, fecha)
- Ver detalle del viaje con:
  - Fecha, destino, descripción
  - Guía asignado
  - Pilotos inscriptos
- (Admin / Editor) ABM de Viajes, con **Soft delete** de viajes en lugar de borrado real, quedan archivados o en borrador.

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
- (Admin / Editor) ABM de los guías

### 6. Página About
- Página estática con info general sobre la empresa

### 7. Messages APP / Chat
- Permite el chat 1:1 entre los usuarios autenticados en la plataforma
- Cada usuario puede seleccionar a quién enviarle un mensaje, como así también ver respuestas e histórico
- La app se usa también para que el usuario info.viajes responda preguntas de interesados a un viaje en particular


---

## Consideraciones técnicas

- Base de datos: SQLite
- Panel de administración: se usará el admin de Django para gestión de usuarios, grupos.
- Frameworks: Django + Bootstrap
- CRUD en frontend para Piloto, Guia y Viajes
- Imágenes de avatar: guardar en `/static/`
- Imágenes de Guías: se guardan en `/media/` (no sincroniza con GitHub)
- Mensajes de confirmación (éxito/error) en las acciones principales utilizando el módulo `messages` de Django


## Tecnologías utilizadas

- Python 3.x
- Django 4.2.x
- SQLite3
- Bootstrap (vía CDN)
- HTML / CSS
- Django Widget Tweaks
- Pillow (para poder usar ImageField)
- Faker (para popular la BD con datos ficticios)

## Estructura de la Aplicación

- **Messages_app**: vistas y templates de la app de chat
- **TikNek_Viajes**: template base, login/logout, home/bienvenida/landing, about
- **Viajes**: vistas y templates de la app que contiene a los Viajes, Guías, Pilotos y la gestión de Usuarios
- **Static**: avatars de los pilotos e imágenes que se usan en la app
- **Media**: imágenes que se suben para los guías (no sincronizada con GH)

## Instalación y ejecución de TikNek_Viajes

### 1. Clonar el repositorio y crear/activar un entorno virtual 
```bash
git clone https://github.com/TikNek1/Coder-TP-Final-Tecco.git
cd TP_Final

# Mac/Linux
python3 -m venv _myenv
source _myenv/bin/activate

# Windows
python -m venv _myenv
_myenv\Scripts\activate
```
###  2. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 3. Lanzar servidor con BD de test y acceder a la app
```bash
python manage.py runserver
http://127.0.0.1:8000/
```
### Opcional - Realizar una limpieza de la BD y cargar algunos datos aleatorios para pruebas.
**ATENCION** no se eliminan los usuarios de la tabla user, solo los modelos específicos. 
Para eliminar usuarios, hacerlos desde consola /admin, cuidado de no borrar el usuario "admin" ni los usuarios del grupo TikNek.
Para encontrarlos fácil, ordenar por el campo "Staff status" en la tabla de usuarios del admin de Django.

Para ejecutar este script, usar el comando:
```bash
python manage.py shell < cargar_datos_fake.py
```
---
