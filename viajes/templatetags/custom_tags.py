from django import template

# Registrar un nuevo módulo de etiquetas y filtros personalizados para usar en los templates de Django
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Filtro personalizado para verificar si un usuario pertenece a un grupo específico.

    Este filtro se utiliza en los templates de Django para controlar el acceso a ciertas
    funcionalidades o elementos de la interfaz, como botones o secciones, dependiendo del
    grupo al que pertenezca el usuario.

    Uso en el template:
    {% if user|has_group:"nombre_del_grupo" %}
        <!-- Contenido visible solo para usuarios del grupo especificado -->
    {% endif %}

    Parámetros:
    - user: El usuario autenticado que se desea verificar.
    - group_name: El nombre del grupo que se desea comprobar.

    Retorna:
    - True si el usuario pertenece al grupo especificado, False en caso contrario.
    """
    return user.groups.filter(name=group_name).exists()